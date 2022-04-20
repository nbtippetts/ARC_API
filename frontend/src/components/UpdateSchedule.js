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
import IconButton from '@mui/material/IconButton';
import EditIcon from '@mui/icons-material/Edit';

const UpdateSchedule = (props) => {
	let product = useSelector((state) => state.product);
	console.log(props)
	const row = props.row;
	console.log(row.IP[0].id)
	const roomId = props.roomId;
	const scheduleId = props.scheduleId;
	const index = props.index;
	const [open, setOpen] = useState(false);
	const [start, setStart] = useState(new Date());
	const [end, setEnd] = useState(new Date());
	const [name, setName] = useState(row.IP[0].name);
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

  	let handleUpdateSchedule = async (e) => {
		e.preventDefault();
		const payload = {
			name: name,
			start_time: start.toLocaleString() + '',
			end_time: end.toLocaleString() + '',
			how_often: '*',
			ip_id: row.IP[0].id
		}
		const response = await axios
		.patch("/room/"+roomId+"/relayschedule/"+scheduleId,payload)
		.catch((err) => {
			console.log("Err: ", err);
		});
		console.log(response);
		if (response.status === 201) {
			product.climate_schedule.splice(index,1)
			product.climate_schedule.push(response.data)
			console.log(product)
			dispatch(setSchedules(product))
		}
		setOpen(false);
	};


	const handleIpSelect=(e)=>{
		setName(e.target.value[1])
  	}

  return (
    <div>
      <IconButton onClick={handleClickOpen}>
        <EditIcon/>
      </IconButton>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Update Schedule</DialogTitle>
		<form onSubmit={handleUpdateSchedule}>
        <DialogContent>
		  <Stack spacing={3}>
          <DialogContentText>
            Update {name}
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
			</Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button type="submit">Update</Button>
        </DialogActions>
		</form>
      </Dialog>
    </div>
  );

};

export default UpdateSchedule;