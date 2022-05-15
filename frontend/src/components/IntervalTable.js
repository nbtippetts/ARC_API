import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useSelector } from "react-redux";
import DeleteInterval from './DeleteInterval';
import UpdateInterval from "./UpdateInterval";

export default function IntervalTable() {
	let product = useSelector((state) => state.product);
	return (
		<TableContainer style={{borderRadius:"20px"}} component={Paper}>
		<Table sx={{ minWidth: 650 }} aria-label="simple table">
			<TableHead>
			<TableRow>
				<TableCell>Name</TableCell>
				<TableCell align="right">Duration</TableCell>
				<TableCell align="right">How Often</TableCell>
				<TableCell align="right">Relay</TableCell>
				<TableCell align="right">Actions</TableCell>
			</TableRow>
			</TableHead>
			<TableBody>
			{product.climate_interval.map((row,index) => (
				<TableRow
				key={row.name}
				sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
				>
				<TableCell component="th" scope="row">
					{row.name}
				</TableCell>
				<TableCell align="right">{row.duration_hour}H:{row.duration_minute}M</TableCell>
				<TableCell align="right">{row.interval_hour}H:{row.interval_minute}M</TableCell>
				{row.IP.map((ip) => (
					<TableCell align="right">{ip.name}</TableCell>
					))}
				<TableCell align="right"><UpdateInterval roomId={product.id} intervalId={row.climate_interval_id} row={row} index={index}/><DeleteInterval roomId={product.id} intervalId={row.climate_interval_id} index={index}/></TableCell>
				</TableRow>
			))}
			</TableBody>
		</Table>
		</TableContainer>
	);
}