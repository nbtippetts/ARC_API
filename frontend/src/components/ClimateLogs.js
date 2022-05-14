import React from "react";
import { useSelector } from "react-redux";
import { DataGrid } from '@mui/x-data-grid'
import { makeStyles } from '@mui/styles';
const useStyles = makeStyles({
    root: {
		"&.MuiDataGrid-root .MuiDataGrid-renderingZone": {
		maxHeight: "none !important"
		},
		"&.MuiDataGrid-root .MuiDataGrid-cell": {
		lineHeight: "unset !important",
		maxHeight: "none !important",
		whiteSpace: "pre-line"
		},
		"&.MuiDataGrid-root .MuiDataGrid-row": {
		maxHeight: "none !important"
		}
  }
});
export const ClimateLogs = () => {
	const classes = useStyles();
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
					{ field: 'humidity', headerName: 'Humidity', flex:1 },
					{ field: 'temperature', headerName: 'Temperature', flex:1 },
					{ field: 'vpd', headerName: 'VPD', flex:1 },
					{ field: 'timestamp', headerName: 'Timestamp', flex:1},
				]

	} else {
		climateColumns = [
					{ field: 'co2', headerName: 'CO2', flex:1 },
					{ field: 'humidity', headerName: 'Humidity', flex:1 },
					{ field: 'temperature', headerName: 'Temperature', flex:1 },
					{ field: 'vpd', headerName: 'VPD', flex:1 },
					{ field: 'timestamp', headerName: 'Timestamp', flex:1 },
				]

	}
	return (
		<div style={{ height: 'auto', overflow: "auto" }}>
			<DataGrid className={classes.root} autoHeight getRowId={(logs) => logs.climate_log_id} rows={logs} columns={climateColumns}
				 pageSize={pageSize}
				onPageSizeChange={(newPageSize) => setPageSize(newPageSize)}
				rowsPerPageOptions={[15, 25, 50, 100]}
				pagination />
		</div>
	)
}
