import React from "react";
import { DataGrid } from '@mui/x-data-grid'
import { useSelector } from "react-redux";
export const ScheduleLogs = () => {
	const [pageSize, setPageSize] = React.useState(5);
	const logs = useSelector((state) => state.allScheduleLogs.scheduleLogs);
		const columns = [
		{ field: 'name', headerName: 'Name', flex:1 },
		{ field: 'start_time', headerName: 'Start', flex:1 },
		{ field: 'end_time', headerName: 'End', flex:1 },
		{ field: 'timestamp', headerName: 'Date', flex:1 },
	]
	return (
		<div style={{ height: 'auto', overflow: "auto" }}>

		<DataGrid autoHeight getRowId={(logs) => logs.climate_schedule_log_id} rows={logs} columns={columns} pageSize={pageSize}
				onPageSizeChange={(newPageSize) => setPageSize(newPageSize)}
				rowsPerPageOptions={[5, 10, 25, 50, 100]}
				pagination />
		</div>
	)
}
