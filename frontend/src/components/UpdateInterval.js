import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Stack from '@mui/material/Stack';
import DurationPicker from 'react-duration-picker'
import { setIntervals } from "../redux/actions/productsActions";
import IconButton from '@mui/material/IconButton';
import EditIcon from '@mui/icons-material/Edit';

const UpdateInterval = (props) => {
	let product = useSelector((state) => state.product);
	console.log(props)
	const row = props.row;
	console.log(row.IP[0].id)
	const roomId = props.roomId;
	const intervalId = props.intervalId;
	const index = props.index;
	const [open, setOpen] = useState(false);
	const [duration, setDuration] = useState({
		hours: 1,
		minutes: 0,
	});
	const [howOften, setHowOften] = useState({
		hours: 1,
		minutes: 0,
	});
	const [name, setName] = useState(row.IP[0].name);
	const dispatch = useDispatch();


	const onDuration = duration => {
		setDuration(duration);
	};
	const onHowOften = howOften => {
		setHowOften(howOften);
	};

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  	let handleUpdateInterval = async (e) => {
		e.preventDefault();
		const payload = {
			name: name,
			duration_hour: duration.hours,
			duration_minute: duration.minutes,
			interval_hour:howOften.hours,
			interval_minute:howOften.minutes,
			ip_id: row.IP[0].id
		}
		const response = await axios
		.patch("/room/"+roomId+"/relayinterval/"+intervalId,payload)
		.catch((err) => {
			console.log("Err: ", err);
		});
		console.log(response);
		if (response.status === 201) {
			product.climate_interval.splice(index,1)
			product.climate_interval.push(response.data)
			console.log(product)
			dispatch(setIntervals(product))
		}
		setOpen(false);
	};

  return (
    <div>
      <IconButton onClick={handleClickOpen}>
        <EditIcon/>
      </IconButton>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Update Interval</DialogTitle>
		<form onSubmit={handleUpdateInterval}>
        <DialogContent>
		  <Stack spacing={3}>
          <DialogContentText>
            Update {name}
          </DialogContentText>
			<DialogContentText>
				Duration
			</DialogContentText>
			<DurationPicker initialDuration={{ hours: 0, minutes: 0, seconds: 0 }} onChange={onDuration}maxHours={12} />
			<DialogContentText>
				How Often
			</DialogContentText>
			<DurationPicker initialDuration={{ hours: 0, minutes: 0, seconds: 0 }} onChange={onHowOften} maxHours={12} />
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

export default UpdateInterval;