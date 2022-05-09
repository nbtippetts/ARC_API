import React from "react";
import { AreaChart, Area,Tooltip, ResponsiveContainer } from 'recharts';
import { useSelector } from "react-redux";
export const VpdChart = () => {
	const logs = useSelector((state) => state.cardLogs.chartLogs);

	return (
		<ResponsiveContainer width="100%" height={75}>
		<AreaChart data={logs}
		margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
		<defs>
			<linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
			<stop offset="5%" stopColor="#ffca28" stopOpacity={0.8}/>
			<stop offset="95%" stopColor="#ffca28" stopOpacity={0}/>
			</linearGradient>
			<linearGradient id="vpdColorPv" x1="0" y1="0" x2="0" y2="1">
			<stop offset="5%" stopColor="#ffc107" stopOpacity={0.8}/>
			<stop offset="95%" stopColor="#ffc107" stopOpacity={0}/>
			</linearGradient>
		</defs>


		<Tooltip />
		<Area type="monotone" dataKey="vpd" stroke="#ffc107" fillOpacity={1} fill="url(#vpdColorPv)" />
		</AreaChart>
		</ResponsiveContainer>
	)
}
