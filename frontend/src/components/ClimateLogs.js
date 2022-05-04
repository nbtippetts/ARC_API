import React from "react";
import { DataGrid } from '@mui/x-data-grid'
import { useSelector } from "react-redux";
export const ClimateLogs = () => {
	const logs = useSelector((state) => state.allClimateLogs.climateLogs);
		const columns = [
		{ field: 'climate_log_id', headerName: 'ID', width: 20 },
		{ field: 'co2', headerName: 'CO2', flex: 1 ,width: 130 },
		{ field: 'humidity', headerName: 'humidity', flex: 1 ,width: 130 },
		{ field: 'temperature', headerName: 'temperature', flex: 1 ,width: 130 },
		{ field: 'timestamp', headerName: 'timestamp', flex: 1 ,width: 130 },
	]
	return (
		<DataGrid autoHeight getRowId={(logs) => logs.climate_log_id} rows={logs} columns={columns} pageSize={25} />
	)
}
