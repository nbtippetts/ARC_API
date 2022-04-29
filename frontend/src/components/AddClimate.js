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

const AddClimate = (props) => {
	let product = useSelector((state) => state.product);
	const roomId = props.roomId;
	const roomIps = props.roomIps;
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

  	let handleClimate = async (e) => {
		e.preventDefault();
		let ips = {
			co2Ip:"",
			humidityIp:"",
			temperatureIp:""
		}
		roomIps.forEach(ip => {
			if (ip.name === "CO2") {
				ips.co2Ip=ip.ip
			} else if (ip.name === "Humidity") {
				ips.humidityIp=ip.ip
			} else if (ip.name === "Temperature") {
				ips.temperatureIp=ip.ip
			}
		})
		const climateResponse = await axios
		.get("/climate_parameters")
		.catch((err) => {
			console.log("Err: ", err);
		});
		if (climateResponse.status === 200) {
			if(climateResponse.data.length === 0){
				var climateId=1
			} else {
				// eslint-disable-next-line no-redeclare
				var climateId=climateResponse.data.length+1
			}
		}
		var payload = {
			name:'test',
			buffer_parameters:buffer,
			co2_parameters:co2,
			co2_buffer_parameters:co2Buffer,
			humidity_parameters:humidity,
			temperature_parameters:temperature,
			climate_start_time:start.toLocaleString() + '',
			climate_end_time:end.toLocaleString() + '',
			co2_relay_ip:ips.co2Ip,
			humidity_relay_ip:ips.humidityIp,
			exhaust_relay_ip:ips.temperatureIp
		}

		const response = await axios
		.put("/room/"+roomId+"/climate/"+climateId,payload)
		.catch((err) => {
			console.log("Err: ", err);
		});
		if (response.status === 201) {
			product.climate.push(response.data)
			console.log(product)
			dispatch(setClimates(product))
		}
		setOpen(false);
	};


  return (
    <div>
      <Button variant="outlined" onClick={handleClickOpen}>
        Create Climate
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Climate</DialogTitle>
		<form onSubmit={handleClimate}>
        <DialogContent>
		  <Stack spacing={3}>
          <DialogContentText>
            Create Your Climate
          </DialogContentText>
		  <TextField id="standard-basic" label="CO2 Buffer" variant="standard" onChange={e => setCo2Buffer(e.target.value)} />
		  <TextField id="standard-basic" label="CO2 Value" variant="standard" onChange={e => setCo2(e.target.value)} />
		  <TextField id="standard-basic" label="Humidity Value" variant="standard" onChange={e => setHumidity(e.target.value)} />
		  <TextField id="standard-basic" label="Temperature Value" variant="standard" onChange={e => setTemperature(e.target.value)} />
		  <TextField id="standard-basic" label="Buffer" variant="standard" onChange={e => setBuffer(e.target.value)} />

			{Object.keys(product.climate).length === 0 ? (
				<div></div>
			) : (
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
			)}
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

export default AddClimate;