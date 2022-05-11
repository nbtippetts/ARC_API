import React from "react";
import { DataGrid } from '@mui/x-data-grid'
import { useSelector } from "react-redux";
export const ClimateLogs = () => {
	const [pageSize, setPageSize] = React.useState(15);
	let setColumns = false
	let logs = useSelector((state) => state.allClimateLogs.climateLogs);
	for (var i = 0; i < logs.length; i++) {
		if (logs[i].co2 === 0) {
			setColumns = true
			break;
		}
		break;
	}
	let climateColumns=[]
	if (setColumns === true){
		climateColumns = [
					{ field: 'climate_log_id', headerName: 'ID', width: 20 },
					{ field: 'humidity', headerName: 'humidity', flex: 1 ,width: 130 },
					{ field: 'temperature', headerName: 'temperature', flex: 1 ,width: 130 },
					{ field: 'vpd', headerName: 'vpd', flex: 1 ,width: 130 },
					{ field: 'timestamp', headerName: 'timestamp', flex: 1 ,width: 130 },
				]

	} else {
		climateColumns = [
					{ field: 'climate_log_id', headerName: 'ID', width: 20 },
					{ field: 'co2', headerName: 'CO2', flex: 1 ,width: 130 },
					{ field: 'humidity', headerName: 'humidity', flex: 1 ,width: 130 },
					{ field: 'temperature', headerName: 'temperature', flex: 1 ,width: 130 },
					{ field: 'vpd', headerName: 'vpd', flex: 1 ,width: 130 },
					{ field: 'timestamp', headerName: 'timestamp', flex: 1 ,width: 130 },
				]

	}
	return (
		<div style={{ height: 400, width: '100%' }}>
			<DataGrid autoHeight getRowId={(logs) => logs.climate_log_id} rows={logs} columns={climateColumns} pageSize={pageSize}
				onPageSizeChange={(newPageSize) => setPageSize(newPageSize)}
				rowsPerPageOptions={[15, 25, 50, 100]}
				pagination />
		</div>
	)
}
