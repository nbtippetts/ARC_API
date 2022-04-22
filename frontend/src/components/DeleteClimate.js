import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { removeClimate } from "../redux/actions/productsActions";
import axios from "axios";
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';



const DeleteClimate = (props) => {
	let product = useSelector((state) => state.product);
	console.log(props)
	const roomId = props.roomId;
	const climateId = props.climateId;
	const index = props.index;
	const dispatch = useDispatch();

	let onDeleteClick = async () => {
		const response = await axios
		.delete("/room/"+roomId+"/climate/"+climateId)
		.catch((err) => {
			console.log("Err: ", err);
		});
		console.log(response);
		if (response.status === 204) {
			product.climate.splice(index,1)
			console.log(product)
			dispatch(removeClimate(product));
		}
	};

	return(
	<IconButton onClick={onDeleteClick}><DeleteIcon/></IconButton>
	);
};

export default DeleteClimate;