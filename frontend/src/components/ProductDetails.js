import React, { useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Stack, Card, CardHeader, CardActionArea, CardContent, Container,Typography,Grid} from '@mui/material';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import OpacityIcon from '@mui/icons-material/Opacity';
import ShowerIcon from '@mui/icons-material/Shower';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import Co2Icon from '@mui/icons-material/Co2';
import QuestionMarkIcon from '@mui/icons-material/QuestionMark';
import CloudIcon from '@mui/icons-material/Cloud';
import {
	selectedProduct,
	removeSelectedProduct
} from "../redux/actions/productsActions";
import { setLogs, setChartLogs } from '../redux/actions/climateLogActions';
import AddInterval from "./AddInterval";
import AddSchedule from "./AddSchedule";
import IntervalTable from "./IntervalTable";
import ScheduleTable from "./ScheduleTable";
import { ClimateChart } from "./ClimateChart";
import { Co2Chart } from "./Co2Chart";
import { HumidityChart } from "./HumidityChart";
import { TemperatureChart } from "./TemperatureChart";
import { makeStyles } from "@mui/styles";
import { ClimateData } from "./ClimateData";
const useStyles = makeStyles(theme => ({
  appBar: {
    top: "auto",
    bottom: 0,
    textAlign:"center"
  },
  overviewcard: {
    display:"flex",
	flexDirection: "column",
    justifyContent:"center",
  }
}));
const ProductDetails = () => {
	const { productId } = useParams();
	let product = useSelector((state) => state.product);
	// const logs = useSelector((state) => state.allLogs.logs);
	const dispatch = useDispatch();
	const classes = useStyles();
	const fetchProductDetail = async (id) => {
		const response = await axios
			.get(`http://localhost:5000/room/${id}`)
			.catch((err) => {
				console.log("Err: ", err);
			});
		dispatch(selectedProduct(response.data));
	};
	const fetchClimateLogs = async (id) => {
		dispatch(setChartLogs([]));
		dispatch(setLogs([]));
		const response = await axios
		.get(`http://localhost:5000/room/${id}/ip_chart_logs`)
		.catch((err) => {
			console.log("Err: ", err);
		});
		if (response.status === 200) {
			const displayLogs = response.data.climate_log[0].slice(0,20)
			dispatch(setChartLogs(displayLogs));
			dispatch(setLogs(response.data.climate_log[0]));
		}
	}
	useEffect(() => {
		if (productId && productId !== "")
		fetchProductDetail(productId);
		fetchClimateLogs(productId);
		return () => {
			dispatch(removeSelectedProduct());
		};
	}, [productId]);

	return (
		<Container maxWidth={false}>
			{Object.keys(product).length === 0 ? (
				<div>...Loading</div>
			) : (
				<Stack spacing={2}>
				<Grid container spacing={2}>
				{product.ip.map((ip,ipIndex) => (
				<Grid item xs={12} sm={6} md={4}>
					<Card elevation={3} sx={{ maxWidth: 345 }}>
						<CardActionArea>
							<CardHeader
							title={ip.name}
							subheader={
								ip.name === "Climate" ? <CloudIcon/> :
								ip.name === "Temperature" ? <ThermostatIcon/> :
								ip.name === "Humidity" ? <OpacityIcon/> :
								ip.name === "CO2" ? <Co2Icon/> :
								ip.name === "Water" ? <ShowerIcon/> :
								ip.name === "Light" ? <LightbulbIcon/> : <QuestionMarkIcon/>
								}>
							</CardHeader>
						<CardContent className={classes.overviewcard}>
							<Typography
								className={"MuiTypography--subheading"}
								 variant={"caption"}>{ip.state.toString()}
							</Typography>
							{ip.name === "Climate" ?
								<ClimateData/>
							:<div></div>}
							{ip.name === "CO2" ?
								<Co2Chart/>
							:<div></div>}
							{ip.name === "Humidity" ?
								<HumidityChart/>
							:<div></div>}
							{ip.name === "Temperature" ?
								<TemperatureChart/>
							:<div></div>}
						</CardContent>
						</CardActionArea>
					</Card>
					</Grid>
				))}

			</Grid>
						<Card elevation={3}>
							<CardContent>
								<ClimateChart roomId={productId} roomIps={product.ip}/>
							</CardContent>
						</Card>
						<AddSchedule roomId={productId}/>
						<ScheduleTable />
						<AddInterval roomId={productId}/>
						<IntervalTable />


			</Stack>
			)}
			</Container>
	);
};

export default ProductDetails;