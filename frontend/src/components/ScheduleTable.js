import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useSelector } from "react-redux";
import DeleteSchedule from './DeleteSchedule';
import UpdateSchedule from "./UpdateSchedule";

export default function ScheduleTable() {
	let product = useSelector((state) => state.product);
	return (
		<TableContainer style={{borderRadius:"20px"}} component={Paper}>
		<Table sx={{ minWidth: 650 }} aria-label="simple table">
			<TableHead>
			<TableRow>
				<TableCell>Name</TableCell>
				<TableCell align="right">Start Time</TableCell>
				<TableCell align="right">End Time</TableCell>
				<TableCell align="right">Relay</TableCell>
				<TableCell align="right">Actions</TableCell>
			</TableRow>
			</TableHead>
			<TableBody>
			{product.climate_schedule.map((row,index) => (
				<TableRow
				key={row.name}
				sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
				>
				<TableCell component="th" scope="row">
					{row.name}
				</TableCell>
				<TableCell align="right">{row.start_time}</TableCell>
				<TableCell align="right">{row.end_time}</TableCell>
				{row.IP.map((ip) => (
					<TableCell align="right">{ip.name}</TableCell>
					))}
				<TableCell align="right"><UpdateSchedule roomId={product.id} scheduleId={row.climate_schedule_id} row={row} index={index}/><DeleteSchedule roomId={product.id} scheduleId={row.climate_schedule_id} index={index}/></TableCell>
				</TableRow>
			))}
			</TableBody>
		</Table>
		</TableContainer>
	);
}