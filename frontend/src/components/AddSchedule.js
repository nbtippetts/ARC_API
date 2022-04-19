import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setIPProducts, removeSelectedIP } from "../redux/actions/productsActions";
import { Dropdown,DropdownButton} from 'react-bootstrap';
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

const AddSchedule = (props) => {
	const [schedule, setSchedule] = useState("");
	let product = useSelector((state) => state.product);
	const roomId = props.roomId;
	const [open, setOpen] = React.useState(false);
	const [start, setStart] = React.useState(new Date());
	const [end, setEnd] = React.useState(new Date());
	const [name, setName] = React.useState("");
	const [ipId, setIpId] = useState("");
	const [ipIndexId, setIpIndexId] = useState("");
	const dispatch = useDispatch();

	const handleChangeName = (newValue) => {
		setName(newValue);
	};
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
		console.log(start)
		console.log(end)
		console.log(name)
		console.log(ipId)

		if(product.climate_schedule.length === 0){
			var scheduleId=1
		} else {
			var scheduleId=product.climate_schedule.length+1
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
		// console.log(response);
		// if (response.status === 201) {
		// }
		setOpen(false);
	};

		const handleSelect=(e)=>{
		console.log(e)
		const indexArr = e.split(",");
		setIpId(indexArr[0]);
		setIpIndexId(indexArr[1]);
  	}

  return (
    <div>
      <Button variant="outlined" onClick={handleClickOpen}>
        Open form dialog
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Schedule</DialogTitle>
		<form onSubmit={handleSchedule}>
        <DialogContent>
          <DialogContentText>
            Create Your Schedule
          </DialogContentText>
		  <Stack spacing={3}>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Name"
            type="text"
            fullWidth
            variant="standard"
			onChange={(e) => setName(e.target.value)}
          />
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
			<DropdownButton
				title="Add To Room"
				id="dropdown-menu-align-right"
				onSelect={handleSelect}>
					{product.ip.map((ip,index) => (
						<Dropdown.Item eventKey={[ip.id,index]}>{ip.name}</Dropdown.Item>
					))}
			</DropdownButton>
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