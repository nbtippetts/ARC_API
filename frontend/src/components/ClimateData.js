import React, {useState} from 'react'
import { io } from 'socket.io-client'
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import OpacityIcon from '@mui/icons-material/Opacity';
import Co2Icon from '@mui/icons-material/Co2';
export const ClimateData = () => {
	// const [co2Data, setCo2Data]=useState("")
	// const [humidityData, setHumidityData]=useState("")
	// const [temperatureData, setTemperatureData]=useState("")
	// const socket = io();
	// socket.connect('http://127.0.0.1/5000')
	// socket.on('connect',function() {
	// 	socket.send()
	// })
	// socket.on('message',function(e) {
	// 	var data = JSON.parse(e)
	// 	setCo2Data(data.co2)
	// 	setHumidityData(data.humidity)
	// 	setTemperatureData(data.temperature)
	// })
  return (
	<div>
		{/* <Stack spacing={1}>
		<Typography
			className={"MuiTypography--subheading"}
			variant={"caption"}>
				<Co2Icon/> {co2Data}ppm
		</Typography>
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
		</Stack> */}
	</div>
  )
}
