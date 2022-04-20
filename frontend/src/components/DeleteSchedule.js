import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { removeSchedule } from "../redux/actions/productsActions";
import axios from "axios";
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';



const DeleteSchedule = (props) => {
	let product = useSelector((state) => state.product);
	console.log(props)
	const roomId = props.roomId;
	const scheduleId = props.scheduleId;
	const index = props.index;
	const dispatch = useDispatch();

	let onDeleteClick = async () => {
		const response = await axios
		.delete("/room/"+roomId+"/relayschedule/"+scheduleId)
		.catch((err) => {
			console.log("Err: ", err);
		});
		console.log(response);
		if (response.status === 204) {
			product.climate_schedule.splice(index,1)
			console.log(product)
			dispatch(removeSchedule(product));
		}
	};

	return(
	<IconButton onClick={onDeleteClick}><DeleteIcon/></IconButton>
	);
};

export default DeleteSchedule;