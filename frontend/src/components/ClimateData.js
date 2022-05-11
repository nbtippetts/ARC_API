import React, {useState, useEffect} from 'react'
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import OpacityIcon from '@mui/icons-material/Opacity';
import Co2Icon from '@mui/icons-material/Co2';
import axios from 'axios';
export const ClimateData = (props) => {
	const id = props.ipId
	const [co2Data, setCo2Data]=useState("")
	const [humidityData, setHumidityData]=useState("")
	const [temperatureData, setTemperatureData]=useState("")
	const [vpdData, setVpdData]=useState("")
	const fetchClimateReads = async () => {
			const response = await axios
			.get(`/climate/reads/${id}`)
			.catch((err) => {
				console.log("Err: ", err);
			});
			if (response.status === 200) {
				if (response.data.co2 === null) {
					setCo2Data("")
					setHumidityData(response.data.humidity)
					setTemperatureData(response.data.temperature)
					setVpdData(response.data.vpd)
				} else {
					setCo2Data(response.data.co2)
					setHumidityData(response.data.humidity)
					setTemperatureData(response.data.temperature)
					setVpdData(response.data.vpd)
				}
			} else {
			}
		}
	useEffect(()=>{
		fetchClimateReads()
		const interval=setInterval(()=>{
		fetchClimateReads()
		},6000)
     return()=>clearInterval(interval)
},[])
  return (
	<div>
		<Stack spacing={2} direction="row" justifyContent="space-around">
		{co2Data === "" ?
			<div style={{display:"none"}}></div>
		:
		<Typography
			className={"MuiTypography--subheading"}
			variant={"caption"}>
				<Co2Icon/> {co2Data}ppm
		</Typography>}
		<Typography
			className={"MuiTypography--subheading"}
			variant={"caption"}>
				<OpacityIcon/>{humidityData}%
		</Typography>
		<Typography
			className={"MuiTypography--subheading"}
			variant={"caption"}>
				<ThermostatIcon/> {temperatureData}&#8457;
		</Typography>
		<Typography
			className={"MuiTypography--subheading"}
			variant={"caption"}>
				<OpacityIcon/>{vpdData} kPa
		</Typography>
		</Stack>
	</div>
  )
}
