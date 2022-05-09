import React from "react";
import { DataGrid } from '@mui/x-data-grid'
import { useSelector } from "react-redux";
export const ClimateLogs = () => {
	const [pageSize, setPageSize] = React.useState(15);
	const logs = useSelector((state) => state.allClimateLogs.climateLogs);
		const columns = [
		{ field: 'climate_log_id', headerName: 'ID', width: 20 },
		{ field: 'co2', headerName: 'CO2', flex: 1 ,width: 130 },
		{ field: 'humidity', headerName: 'humidity', flex: 1 ,width: 130 },
		{ field: 'temperature', headerName: 'temperature', flex: 1 ,width: 130 },
		{ field: 'vpd', headerName: 'vpd', flex: 1 ,width: 130 },
		{ field: 'timestamp', headerName: 'timestamp', flex: 1 ,width: 130 },
	]
	return (
		<div style={{ height: 400, width: '100%' }}>
			<DataGrid autoHeight getRowId={(logs) => logs.climate_log_id} rows={logs} columns={columns} pageSize={pageSize}
				onPageSizeChange={(newPageSize) => setPageSize(newPageSize)}
				rowsPerPageOptions={[15, 25, 50, 100]}
				pagination />
		</div>
	)
}
