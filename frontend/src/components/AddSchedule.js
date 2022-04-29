import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
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
import { setSchedules } from "../redux/actions/productsActions";

const AddSchedule = (props) => {
	let product = useSelector((state) => state.product);
	const roomId = props.roomId;
	const [open, setOpen] = useState(false);
	const [start, setStart] = useState(new Date());
	const [end, setEnd] = useState(new Date());
	const [name, setName] = useState("");
	const [ipId, setIpId] = useState("");
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

  	let handleSchedule = async (e) => {
		e.preventDefault();
		const scheduleResponse = await axios
		.get("/relayschedule")
		.catch((err) => {
			console.log("Err: ", err);
		});
		if (scheduleResponse.status === 200) {
			if(scheduleResponse.data.length === 0){
				var scheduleId=1
			} else {
				// eslint-disable-next-line no-redeclare
				var scheduleId=scheduleResponse.data.length+1
			}
		}
		const payload = {
			name: name,
			start_time: start.toLocaleString() + '',
			end_time: end.toLocaleString() + '',
			how_often: '*',
			ip_id: ipId
		}
		const response = await axios
		.put("/room/"+roomId+"/relayschedule/"+scheduleId,payload)
		.catch((err) => {
			console.log("Err: ", err);
		});
		console.log(response);
		if (response.status === 201) {
			product.climate_schedule.push(response.data)
			console.log(product)
			dispatch(setSchedules(product))
		}
		setOpen(false);
	};


	const handleIpSelect=(key,value)=>{
		setIpId(key);
		setName(value)
  	}

  return (
    <div>
      <Button variant="outlined" onClick={handleClickOpen}>
        Create Schedule
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Schedule</DialogTitle>
		<form onSubmit={handleSchedule}>
        <DialogContent>
		  <Stack spacing={3}>
          <DialogContentText>
            Create Your Schedule
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
			<Select
				title="Relay"
				id="dropdown-menu-align-right"
				label="Add To Relay">
					{product.ip.map((ip) => (
						<MenuItem onClick={() => handleIpSelect(ip.id,ip.name)} value={ip.name}>{ip.name}</MenuItem>
					))}
				</Select>
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

export default AddSchedule;