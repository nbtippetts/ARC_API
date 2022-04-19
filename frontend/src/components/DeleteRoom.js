import React from "react";
import { useDispatch } from "react-redux";
import { removeSelectedProduct } from "../redux/actions/productsActions";
import axios from "axios";
import { Button} from 'react-bootstrap';


const DeleteRoom = (props) => {
	const id = props.roomId;
	const indexId = props.indexId;
	const dispatch = useDispatch();
	let onDeleteClick = async (id) => {
		console.log(id)
		const response = await axios
			.delete("http://localhost:5000/room/"+id)
			.catch((err) => {
				console.log("Err: ", err);
				});
				console.log(response);
				if (response.status === 204) {
					console.log(response.status)
					dispatch(removeSelectedProduct(indexId));
				}
		}

		return (
			<Button variant="danger" key={id} onClick={()=>onDeleteClick(id)}>Delete</Button>
		);
};

export default DeleteRoom;