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
import TextField from '@mui/material/TextField';
import { selectedNote } from "../redux/actions/NoteBookActions";
import IconButton from '@mui/material/IconButton';
import EditIcon from '@mui/icons-material/Edit';

const UpdateNote = (props) => {
	let notes = useSelector((state) => state.notes.notes);
	const roomId = props.roomId;
	const noteId = props.noteId;
	const noteIndex = props.noteIndex;
	const [title, setTitle] = useState("");
	const [body, setBody] = useState("");
	const [open, setOpen] = useState(false);
	const CHARACTER_LIMIT = 225;
	const dispatch = useDispatch();

	 const handleClickOpen = () => {
		setOpen(true);
	};

	const handleClose = () => {
		setOpen(false);
	};
  	let handleUpdateNote = async (e) => {
		e.preventDefault();
		const payload = {
			title: title,
			body: body,
		}
		const response = await axios
		.patch("/room/"+roomId+"/note/"+noteId,payload)
		.catch((err) => {
			console.log("Err: ", err);
		});
		if (response.status === 201) {
			notes.splice(noteIndex,1)
			notes.push(response.data)
			dispatch(selectedNote(notes))
		}
		setOpen(false);
		setTitle("")
		setBody("")
	};

  return (
    <div>
      <IconButton onClick={handleClickOpen}>
        <EditIcon/>
      </IconButton>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Update Note</DialogTitle>
		<form onSubmit={handleUpdateNote}>
        <DialogContent>
		  <Stack spacing={3}>
          <DialogContentText>
            <TextField
				label={"Title"}
				value={title}
				onChange={e => setTitle(e.target.value)}
				variant="standard"
				size="small"/>
			</DialogContentText>
			<DialogContentText>
				<TextField
					label={"Note"}
					placeholder="Note To Self"
					multiline={true}
					minRows={5}
					fullWidth={true}
					inputProps={{
						maxlength: CHARACTER_LIMIT,
					}}
					value={body}
					helperText={`${body.length}/${CHARACTER_LIMIT}`}
					onChange={e => setBody(e.target.value)}

				/>
			</DialogContentText>
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

export default UpdateNote;