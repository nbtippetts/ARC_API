import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useSelector } from "react-redux";
import DeleteClimate from './DeleteClimate';
import UpdateClimate from './UpdateClimate';
import moment from 'moment';


export default function ClimateTable() {
	let product = useSelector((state) => state.product);
	const handleDate=(value)=>{
		var climateDate = moment(value,'HH:mm:ss').format('hh:mm a');
		return climateDate
  	}
	return (
		<TableContainer component={Paper}>
		<Table sx={{ minWidth: 650 }} aria-label="simple table">
			<TableHead>
			<TableRow>

				<TableCell>Name</TableCell>
				<TableCell align="right">Co2 Buffer</TableCell>
				<TableCell align="right">Co2</TableCell>
				<TableCell align="right">Humidity</TableCell>
				<TableCell align="right">Exhaust</TableCell>
				<TableCell align="right">buffer</TableCell>
				<TableCell align="right">Night Start</TableCell>
				<TableCell align="right">Night End</TableCell>
				<TableCell align="right">Actions</TableCell>
			</TableRow>
			</TableHead>
			<TableBody>
			{product.climate.map((row,index) => (
				<TableRow
				key={row.name}
				sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
				>
				<TableCell component="th" scope="row">
					{row.name}
				</TableCell>
				<TableCell align="right">{row.co2_buffer_parameters}</TableCell>
				<TableCell align="right">{row.co2_parameters}</TableCell>
				<TableCell align="right">{row.humidity_parameters}</TableCell>
				<TableCell align="right">{row.temperature_parameters}</TableCell>
				<TableCell align="right">{row.buffer_parameters}</TableCell>

					<TableCell align="right">{row.climate_day_night.map((climateTime) => (
						handleDate(climateTime.climate_start_time)
						))}
					</TableCell>
					<TableCell align="right">{row.climate_day_night.map((climateTime) => (
						handleDate(climateTime.climate_end_time)
						))}
					</TableCell>

				<TableCell align="right">
					<UpdateClimate roomId={product.id} climateId={row.climate_id} exhaust_relay_ip={row.exhaust_relay_ip} co2_relay_ip={row.co2_relay_ip} humidity_relay_ip={row.humidity_relay_ip} index={index}/>
					<DeleteClimate roomId={product.id} climateId={row.climate_id} index={index}/>
				</TableCell>
				</TableRow>
			))}
			</TableBody>
		</Table>
		</TableContainer>
	);
}