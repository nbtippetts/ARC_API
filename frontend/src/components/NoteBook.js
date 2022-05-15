import React from 'react'
import Timeline from '@mui/lab/Timeline';
import TimelineItem from '@mui/lab/TimelineItem';
import TimelineSeparator from '@mui/lab/TimelineSeparator';
import TimelineConnector from '@mui/lab/TimelineConnector';
import TimelineContent from '@mui/lab/TimelineContent';
import TimelineDot from '@mui/lab/TimelineDot';
import { useSelector } from "react-redux";
import { Card,CardHeader,CardContent } from '@mui/material';
import { makeStyles } from "@mui/styles";
import AddNote from "./AddNote";
import DeleteNote from './DeleteNote';
import UpdateNote from "./UpdateNote";
import Stack from '@mui/material/Stack';

const useStyles = makeStyles(theme => ({
  overviewcard: {
	height: "100%",
  width:"100%",
    display:"flex",
	flexDirection: "column",
},
}));

const NoteBook = (props) => {
  const roomId = props.roomId;
	const notes = useSelector((state) => state.notes.notes);
  let note = useSelector((state) => state.note);
	const classes = useStyles();
  return (
    <Card elevation={3} style={{borderRadius:"20px"}}>
      <Stack spacing={2}>
      <AddNote roomId={roomId}/>
    	{Object.keys(notes).length === 0 ? (
				<div></div>
			) : (
        <div>
        <Timeline position="alternate" sx={{ display: { xs: 'none', md: 'none', lg: 'block' }}}>
          {notes.map((note,index) => (
          <TimelineItem>
            <TimelineSeparator>
              <TimelineDot />
              <TimelineConnector />
            </TimelineSeparator>
                <TimelineContent>
                <Card elevation={3} style={{borderRadius:"20px"}} align="left" className={classes.overviewcard}>
                  <CardHeader action={
                    <Stack>
                      <DeleteNote roomId={roomId} noteId={note.notebook_id} noteIndex={index}/>
                      <UpdateNote roomId={roomId} noteId={note.notebook_id} noteIndex={index}/>
                      </Stack>
                  }
                  title={note.title}
                  subheader={note.publish_date}
                  >
                  </CardHeader>
                  <CardContent>
                    {note.body}
                  </CardContent>
                </Card>
            </TimelineContent>
          </TimelineItem>
            ))}
          </Timeline>
        <Stack spacing={2} sx={{ display: { xs: 'block', md: 'block', lg: 'none' }}}>
            {notes.map((note,index) => (
                <Card elevation={3} style={{borderRadius:"20px"}} align="left" className={classes.overviewcard}>
                  <CardHeader action={
                    <Stack>
                      <DeleteNote roomId={roomId} noteId={note.notebook_id} noteIndex={index}/>
                      <UpdateNote roomId={roomId} noteId={note.notebook_id} noteIndex={index}/>
                      </Stack>
                  }
                  title={note.title}
                  subheader={note.publish_date}
                  >
                  </CardHeader>
                  <CardContent>
                    {note.body}
                  </CardContent>
                </Card>
            ))}
         </Stack>
          </div>
      )}
      </Stack>
      </Card>
  );
}
export default NoteBook;