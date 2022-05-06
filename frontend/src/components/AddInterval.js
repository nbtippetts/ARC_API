import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Stack from '@mui/material/Stack';
import DurationPicker from 'react-duration-picker'
import { setIntervals } from "../redux/actions/productsActions";


const AddInterval = (props) => {
	let product = useSelector((state) => state.product);
	const roomId = props.roomId;
	const [open, setOpen] = useState(false);
	const [duration, setDuration] = useState({
		hours: 1,
		minutes: 0,
	});
	const [howOften, setHowOften] = useState({
		hours: 1,
		minutes: 0,
	});
	const [name, setName] = useState("");
	const [ipId, setIpId] = useState("");
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

  	let handleInterval = async (e) => {
		e.preventDefault();
		const payload = {
			name: name,
			duration_hour: duration.hours,
			duration_minute: duration.minutes,
			interval_hour:howOften.hours,
			interval_minute:howOften.minutes,
			ip_id: ipId
		}
		const intervalId=0
		const response = await axios
		.put("/room/"+roomId+"/relayinterval/"+intervalId,payload)
		.catch((err) => {
			console.log("Err: ", err);
		});
		console.log(response);
		if (response.status === 201) {
			product.climate_interval.push(response.data)
			console.log(product)
			dispatch(setIntervals(product))
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
        Create Interval
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Interval Schedule</DialogTitle>
		<form onSubmit={handleInterval}>
        <DialogContent>
		  <Stack spacing={3}>
          <DialogContentText>
            Duration
          </DialogContentText>
		  <DurationPicker initialDuration={{ hours: 0, minutes: 0, seconds: 0 }} onChange={onDuration}maxHours={12} />
          <DialogContentText>
            How Often
          </DialogContentText>
		  <DurationPicker initialDuration={{ hours: 0, minutes: 0, seconds: 0 }} onChange={onHowOften} maxHours={12} />
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

export default AddInterval;