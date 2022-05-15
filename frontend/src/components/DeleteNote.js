/* eslint-disable array-callback-return */
import React from "react";
import { useDispatch} from "react-redux";
import axios from "axios";
import IconButton from '@mui/material/IconButton';
import DeleteOutlined from '@mui/icons-material/DeleteOutlined';
import { removeNote } from "../redux/actions/NoteBookActions";



const DeleteNote = (props) => {
	const id = props.noteId;
	const noteIndex = props.noteIndex;
	const roomId = props.roomId;
	const dispatch = useDispatch();

	let onDeleteClick = async (id) => {
		const response = await axios
		.delete("/room/"+roomId+"/note/"+id)
		.catch((err) => {
			console.log("Err: ", err);
		});
		console.log(response);
		if (response.status === 204) {
			dispatch(removeNote(noteIndex));
		}
	};

	return(
	<IconButton variant="danger" key={id} onClick={()=>onDeleteClick(id)}><DeleteOutlined/></IconButton>
	);
};

export default DeleteNote;