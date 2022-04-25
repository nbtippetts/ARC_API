import React from "react";
import { AreaChart, Area,Tooltip, ResponsiveContainer, XAxis, YAxis, CartesianGrid } from 'recharts';
import AddClimate from "./AddClimate";
import ClimateTable from "./ClimateTable";
import { DataGrid } from '@mui/x-data-grid'
import { Grid} from '@mui/material';
import { useSelector } from "react-redux";
export const ClimateChart = (props) => {
	const productId = props.productId
	const roomIps = props.roomIps
	const logs = useSelector((state) => state.allLogs.logs);
	const columns = [
		{ field: 'climate_log_id', headerName: 'ID', width: 70 },
		{ field: 'co2', headerName: 'CO2', width: 130 },
		{ field: 'humidity', headerName: 'humidity', width: 130 },
		{ field: 'temperature', headerName: 'temperature', width: 130 },
		{ field: 'timestamp', headerName: 'timestamp', width: 130 },
	]
	return (
	<Grid container spacing={2 }direction="row" justify="center" alignItems="stretch">
		<Grid item xs={12} sm={12} md={8}>
			<Grid container spacing={3}>
				<Grid item xs={12}>
				<ResponsiveContainer width="100%" height={450}>
				<AreaChart data={logs}
					margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
					<defs>
						<linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
						<stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
						<stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
						</linearGradient>
						<linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
						<stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
						<stop offset="95%" stopColor="#82ca9d" stopOpacity={0}/>
						</linearGradient>
					</defs>

				<XAxis dataKey="timestamp" />
				<YAxis />
				<CartesianGrid strokeDasharray="3 3" />
				<Tooltip />
				<Area type="monotone" dataKey="co2" stroke="#82ca9d" fillOpacity={1} fill="url(#colorPv)" />
				<Area type="monotone" dataKey="humidity" stroke="#82ca9d" fillOpacity={1} fill="url(#colorPv)" />
				<Area type="monotone" dataKey="temperature" stroke="#82ca9d" fillOpacity={1} fill="url(#colorPv)" />
				</AreaChart>
				</ResponsiveContainer>
				</Grid>
				<Grid item xs={12}>
					<AddClimate roomId={productId} roomIps={roomIps}/>
					<ClimateTable />
				</Grid>
			</Grid>
		</Grid>
		<Grid item xs={12} sm={12} md={4}>
			<Grid style={{ display: 'flex', height: '100%',flexGrow: 1  }}>
				<DataGrid getRowId={(logs) => logs.climate_log_id} rows={logs} columns={columns} pageSize={25} />
			</Grid>
		</Grid>
		</Grid>
	)
}
