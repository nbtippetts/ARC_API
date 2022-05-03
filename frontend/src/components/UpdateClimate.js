import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Stack from '@mui/material/Stack';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { setClimates } from "../redux/actions/productsActions";
import IconButton from '@mui/material/IconButton';
import EditIcon from '@mui/icons-material/Edit';

const UpdateClimate = (props) => {
	let product = useSelector((state) => state.product);
	const temperatureIp = props.exhaust_relay_ip
	const co2Ip = props.co2_relay_ip
	const humidityIp = props.humidity_relay_ip
	const roomId = props.roomId;
	const climateId = props.climateId;
	const index = props.index;
	const [open, setOpen] = useState(false);
	const [start, setStart] = useState(new Date());
	const [end, setEnd] = useState(new Date());
	const [buffer, setBuffer] = useState("");
	const [co2Buffer, setCo2Buffer] = useState("");
	const [co2, setCo2] = useState("");
	const [humidity, setHumidity] = useState("");
	const [temperature, setTemperature] = useState("");
	const dispatch = useDispatch();


	const handleChangeStart = (newValue) => {
		setStart(newValue);
	};
	const handleChangeEnd = (newValue) => {
		setEnd(newValue);
	};

	const handleClickOpen = () => {
		setOpen(true);
	};

	const handleClose = () => {
		setOpen(false);
	};

  	let handleUpdateClimate = async (e) => {
		e.preventDefault();
		var payload = {
			name:'test',
			buffer_parameters:buffer,
			co2_parameters:co2,
			co2_buffer_parameters:co2Buffer,
			humidity_parameters:humidity,
			temperature_parameters:temperature,
			climate_start_time:start.toLocaleString() + '',
			climate_end_time:end.toLocaleString() + '',
			co2_relay_ip:co2Ip,
			humidity_relay_ip:humidityIp,
			exhaust_relay_ip:temperatureIp
		}
		const response = await axios
		.patch("/room/"+roomId+"/climate/"+climateId,payload)
		.catch((err) => {
			console.log("Err: ", err);
		});
		console.log(response);
		if (response.status === 201) {
			product.climate.splice(index,1)
			product.climate.push(response.data)
			console.log(product)
			dispatch(setClimates(product))
		}
		setOpen(false);
	};
// eslint-disable-next-line array-callback-return
const renderList = product.climate.map((climateTime,index) => {
	if(climateTime.climate_day_night.length !== 0) {
		return (
		<div>
			<DialogContentText>
				Night Time Parameters
			</DialogContentText>
			<LocalizationProvider dateAdapter={AdapterDateFns}>
				<TimePicker
				label="Start Time"
				value={start}
				onChange={handleChangeStart}
				renderInput={(params) => <TextField {...params} />}
				/>
				<TimePicker
				label="End Time"
				value={end}
				onChange={handleChangeEnd}
				renderInput={(params) => <TextField {...params} />}
				/>
			</LocalizationProvider>
		</div>
		)
	}
})
  return (
    <div>
      <IconButton onClick={handleClickOpen}>
        <EditIcon/>
      </IconButton>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Climate</DialogTitle>
		<form onSubmit={handleUpdateClimate}>
        <DialogContent>
		  <Stack spacing={3}>
          <DialogContentText>
            Update Your Climate
          </DialogContentText>
		  <TextField id="standard-basic" label="CO2 Buffer" variant="standard" onChange={e => setCo2Buffer(e.target.value)} />
		  <TextField id="standard-basic" label="CO2 Value" variant="standard" onChange={e => setCo2(e.target.value)} />
		  <TextField id="standard-basic" label="Humidity Value" variant="standard" onChange={e => setHumidity(e.target.value)} />
		  <TextField id="standard-basic" label="Temperature Value" variant="standard" onChange={e => setTemperature(e.target.value)} />
		  <TextField id="standard-basic" label="Buffer" variant="standard" onChange={e => setBuffer(e.target.value)} />
			<>{renderList}</>
		</Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button type="submit">ADD</Button>
        </DialogActions>
		</form>
      </Dialog>
    </div>
  );

};

export default UpdateClimate;