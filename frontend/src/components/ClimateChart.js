import React from "react";
import { AreaChart, Area,Tooltip, ResponsiveContainer, XAxis, YAxis, CartesianGrid } from 'recharts';
import { useSelector } from "react-redux";
export const ClimateChart = () => {
	const logs = useSelector((state) => state.cardLogs.chartLogs);
	return (
		<ResponsiveContainer width="100%" height={450}>
		<AreaChart data={logs}
			margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
			<defs>
				<linearGradient id="co2ColorUv" x1="0" y1="0" x2="0" y2="1">
				<stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
				<stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
				</linearGradient>
				<linearGradient id="co2ColorPv" x1="0" y1="0" x2="0" y2="1">
				<stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
				<stop offset="95%" stopColor="#82ca9d" stopOpacity={0}/>
				</linearGradient>
				<linearGradient id="humidityColorUv" x1="0" y1="0" x2="0" y2="1">
				<stop offset="5%" stopColor="#42a5f5" stopOpacity={0.8}/>
				<stop offset="95%" stopColor="#42a5f5" stopOpacity={0}/>
				</linearGradient>
				<linearGradient id="humidityColorPv" x1="0" y1="0" x2="0" y2="1">
				<stop offset="5%" stopColor="#2196f3" stopOpacity={0.8}/>
				<stop offset="95%" stopColor="#2196f3" stopOpacity={0}/>
				</linearGradient>
				<linearGradient id="TemperatureColorUv" x1="0" y1="0" x2="0" y2="1">
				<stop offset="5%" stopColor="#ef5350" stopOpacity={0.8}/>
				<stop offset="95%" stopColor="#ef5350" stopOpacity={0}/>
				</linearGradient>
				<linearGradient id="TemperatureColorPv" x1="0" y1="0" x2="0" y2="1">
				<stop offset="5%" stopColor="#f44336" stopOpacity={0.8}/>
				<stop offset="95%" stopColor="#f44336" stopOpacity={0}/>
				</linearGradient>
			</defs>

		<XAxis dataKey="timestamp" />
		<YAxis yAxisId="left" />
		<YAxis yAxisId="right" orientation="right" />
		<CartesianGrid strokeDasharray="3 3" />
		<Tooltip />
		<Area yAxisId="left" type="monotone" dataKey="co2" stroke="#82ca9d" fillOpacity={1} fill="url(#co2ColorPv)" />
		<Area yAxisId="right" type="monotone" dataKey="humidity" stroke="#2196f3" fillOpacity={1} fill="url(#humidityColorPv)" />
		<Area yAxisId="right" type="monotone" dataKey="temperature" stroke="#f44336" fillOpacity={1} fill="url(#TemperatureColorPv)" />
		</AreaChart>
		</ResponsiveContainer>
	)
}
