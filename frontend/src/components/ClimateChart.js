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
				<linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
				<stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
				<stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
				</linearGradient>
				<linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
				<stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
				<stop offset="95%" stopColor="#82ca9d" stopOpacity={0}/>
				</linearGradient>
			</defs>

		<XAxis dataKey="timestamp" />
		<YAxis />
		<CartesianGrid strokeDasharray="3 3" />
		<Tooltip />
		<Area type="monotone" dataKey="co2" stroke="#82ca9d" fillOpacity={1} fill="url(#colorPv)" />
		<Area type="monotone" dataKey="humidity" stroke="#82ca9d" fillOpacity={1} fill="url(#colorPv)" />
		<Area type="monotone" dataKey="temperature" stroke="#82ca9d" fillOpacity={1} fill="url(#colorPv)" />
		</AreaChart>
		</ResponsiveContainer>
	)
}
