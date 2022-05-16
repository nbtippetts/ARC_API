import React, { useState,useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import { setNotes } from "../redux/actions/NoteBookActions";
import Box from "@mui/material/Box";
import AddCircleOutlineRoundedIcon from '@mui/icons-material/AddCircleOutlineRounded';
import IconButton from '@mui/material/IconButton';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { StaticDatePicker } from '@mui/x-date-pickers/StaticDatePicker';
import { makeStyles } from "@mui/styles";
const useStyles = makeStyles(theme => ({
  input2: {
    height: "280px",
  }
}));
const AddNote = (props) => {
	const classes = useStyles();
	const notes = useSelector((state) => state.notes.notes);
	const roomId = props.roomId;
	const [title, setTitle] = useState("");
	const [body, setBody] = useState("");
	const [noteDate, setNoteDate] = useState(new Date());
	const CHARACTER_LIMIT = 225;
	const dispatch = useDispatch();

	const handleTitle = (event) => {
		setTitle(event.target.value);
	};
	const handleBody = (event) => {
		setBody(event.target.value);
	};
  	let handleNote = async (e) => {
		const payload = {
			title: title,
			body: body,
		}
		const response = await axios
		.put("/room/"+roomId+"/note/1",payload)
		.catch((err) => {
			console.log("Err: ", err);
		});
		if (response.status === 201) {
			dispatch(setNotes([...notes, response.data]))
			setTitle("")
			setBody("")
		}
	};
	let handleNoteDate = async (e) => {
		const payload = {
			noteDate: noteDate,
		}
		const response = await axios
		.get("/room/"+roomId+"/notes",{params: payload})
		.catch((err) => {
			dispatch(setNotes([]));
		});
		if (response.status === 200) {
			dispatch(setNotes(response.data));
		}
	};
	useEffect(() => {
		handleNoteDate();
	}, [noteDate]);
  return (
<Grid container spacing={2} direction="row" justifyContent="space-around" alignItems="stretch">
	<Grid item xs={12} sm={12} lg={6}>
	<Card elevation={0} align="left" style={{borderRadius:"20px", height:"100%"}}>
      <CardHeader
			action={
					<IconButton variant="danger" onClick={handleNote}><AddCircleOutlineRoundedIcon/></IconButton>
			}
			title={
			<TextField
				label={"Title"}
				value={title}
				onChange={handleTitle}
				variant="standard"
				size="small"/>
			}>
		</CardHeader>
		<CardContent>
			<TextField
				label={"Note"}
				placeholder="Note To Self"
				multiline={true}
				minRows={5}
				fullWidth={true}
				inputProps={{
					maxlength: CHARACTER_LIMIT,
				}}
				InputProps={{
					classes: { input: classes.input2 },
				}}
				value={body}
				helperText={`${body.length}/${CHARACTER_LIMIT}`}
				onChange={handleBody}

			/>
		<Box sx={{ display: { xs: 'block', md: 'block', lg: 'none' }}}>
			<LocalizationProvider dateAdapter={AdapterDateFns}>
				<StaticDatePicker
					orientation="portrait"
					openTo="day"
					value={noteDate}
					onChange={(newValue) => {
						setNoteDate(newValue);
					}}
					renderInput={(params) => <TextField {...params} />}
				/>
			</LocalizationProvider>
			</Box>
		</CardContent>
	</Card>
	</Grid>
		<Box sx={{ display: { xs: 'none', md: 'none', lg: 'block' }}}>
		<Grid item xs={12} sm={12} lg={6}>
			<LocalizationProvider dateAdapter={AdapterDateFns}>
				<StaticDatePicker
					orientation="portrait"
					openTo="day"
					value={noteDate}
					onChange={(newValue) => {
						setNoteDate(newValue);
					}}
					renderInput={(params) => <TextField {...params} />}
				/>
			</LocalizationProvider>
			</Grid>
		</Box>
</Grid>
  );

};

export default AddNote;