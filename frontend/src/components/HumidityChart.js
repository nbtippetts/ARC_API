import React from "react";
import { AreaChart, Area,Tooltip, ResponsiveContainer } from 'recharts';
import { useSelector } from "react-redux";
export const HumidityChart = () => {
	const logs = useSelector((state) => state.cardLogs.chartLogs);
	return (
		<ResponsiveContainer width="100%" height={75}>
		<AreaChart data={logs}
		margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
		<defs>
			<linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
			<stop offset="5%" stopColor="#42a5f5" stopOpacity={0.8}/>
			<stop offset="95%" stopColor="#42a5f5" stopOpacity={0}/>
			</linearGradient>
			<linearGradient id="humidityColorPv" x1="0" y1="0" x2="0" y2="1">
			<stop offset="5%" stopColor="#2196f3" stopOpacity={0.8}/>
			<stop offset="95%" stopColor="#2196f3" stopOpacity={0}/>
			</linearGradient>
		</defs>


		<Tooltip />
		<Area type="monotone" dataKey="humidity" stroke="#2196f3" fillOpacity={1} fill="url(#humidityColorPv)" />
		</AreaChart>
		</ResponsiveContainer>
	)
}
