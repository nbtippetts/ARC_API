import React from "react";
import { DataGrid } from '@mui/x-data-grid'
import { useSelector } from "react-redux";
export const ScheduleLogs = () => {
	const logs = useSelector((state) => state.allScheduleLogs.scheduleLogs);
		const columns = [
		{ field: 'climate_schedule_log_id', headerName: 'ID', width: 70 },
		{ field: 'name', headerName: 'Name', width: 130 },
		{ field: 'start_time', headerName: 'Start', width: 130 },
		{ field: 'end_time', headerName: 'End', width: 130 },
	]
	return (
		<DataGrid autoHeight getRowId={(logs) => logs.climate_schedule_log_id} rows={logs} columns={columns} pageSize={25} />
	)
}
