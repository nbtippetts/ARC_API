/* eslint-disable array-callback-return */
import React from "react";
import { useDispatch } from "react-redux";
import { removeSelectedIP } from "../redux/actions/productsActions";
import axios from "axios";
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import DeleteOutlined from '@mui/icons-material/DeleteOutlined';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Slide from '@mui/material/Slide';
import Typography from '@mui/material/Typography';
import FileDownloadRoundedIcon from '@mui/icons-material/FileDownloadRounded';

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const PurgeIP = (props) => {
	const id = props.ipId;
	const ipIndexId = props.indexId;
	const dispatch = useDispatch();
	const [open, setOpen] = React.useState(false);

	let onDeleteClick = async (id) => {
		const response = await axios
		.delete("/delete_ip/"+id)
		.catch((err) => {
			console.log("Err: ", err);
		});
		console.log(response);
		if (response.status === 204) {
			dispatch(removeSelectedIP(ipIndexId));
			setOpen(false);
		}
	};

	const handleClickOpen = () => {
		setOpen(true);
	};

	const handleClose = () => {
		setOpen(false);
	};
	return(
		<div>
		<IconButton variant="danger" onClick={handleClickOpen}><DeleteOutlined/></IconButton>
		<Dialog
			open={open}
			TransitionComponent={Transition}
			keepMounted
			onClose={handleClose}
			aria-describedby="alert-dialog-slide-description"
		>
			<DialogTitle>{"Hold UP! I, Me, Myself and I are not responsible.\nViewer Discretion Is Advised"}</DialogTitle>
			<DialogContent>
			<DialogContentText id="alert-dialog-slide-description">
				<Typography>
					Well Boyz here we are.
				</Typography>
				<Typography>
					Think about it for a minute... Still want to delete this relay and all it's associated data?
				</Typography>
				<Typography>
				</Typography>
				<Typography>
					The following data will be forever lost in The Warren of Chaos,
				</Typography>
				<Typography>
					Climate Logs, Schedule Logs, The Pretty Line In The Chart
				</Typography>
				<Typography>
					If you want to keep your historical data on file you can download it by clicking this Icon<IconButton><FileDownloadRoundedIcon/></IconButton>
				</Typography>
				<Typography>
					Remember if you accidentally delete a relay you can re-registor if by turning it of and on again.
				</Typography>
			</DialogContentText>
			</DialogContent>
			<DialogActions>
			<Button onClick={handleClose}>Not Today</Button>
			<Button  key={id} onClick={()=>onDeleteClick(id)}>To The Abyss</Button>
			</DialogActions>
		</Dialog>
		</div>
	);
};

export default PurgeIP;