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
import { setScheduleLogs,setClimateLogs, setChartLogs } from '../redux/actions/climateLogActions';
import AddInterval from "./AddInterval";
import AddSchedule from "./AddSchedule";
import IntervalTable from "./IntervalTable";
import ScheduleTable from "./ScheduleTable";
import { ClimateChart } from "./ClimateChart";
import { ScheduleLogs } from "./ScheduleLogs";
import { Co2Chart } from "./Co2Chart";
import { HumidityChart } from "./HumidityChart";
import { TemperatureChart } from "./TemperatureChart";
import { makeStyles } from "@mui/styles";
// import { ClimateData } from "./ClimateData";
import AddClimate from "./AddClimate";
import ClimateTable from "./ClimateTable";
import { ClimateLogs } from "./ClimateLogs";
import { RelayControl } from "./RelayControl";

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
	const dispatch = useDispatch();
	const classes = useStyles();
	// eslint-disable-next-line react-hooks/exhaustive-deps
	const fetchProductDetail = async (id) => {
		const response = await axios
			.get(`/room/${id}`)
			.catch((err) => {
				console.log("Err: ", err);
			});
		dispatch(selectedProduct(response.data));
	};
	// eslint-disable-next-line react-hooks/exhaustive-deps
	const fetchClimateLogs = async (id) => {
		const response = await axios
		.get(`/room/${id}/ip_chart_logs`)
		.catch((err) => {
			console.log("Err: ", err);
		});
		if (response.status === 200) {
			dispatch(setClimateLogs(response.data.climate_log[0]));
			const displayLogs = response.data.climate_log[0].slice(0,20)
			dispatch(setChartLogs(displayLogs.reverse()));
		}
	}
	const fetchScheduleLogs = async (id) => {
		const response = await axios
		.get(`/room/${id}/ip_logs`)
		.catch((err) => {
			console.log("Err: ", err);
		});
		if (response.status === 200) {
			// console.log(response.data.climate_schedule_log[0])
			dispatch(setScheduleLogs(response.data.climate_schedule_log));
		}
	}
	useEffect(() => {
		if (productId && productId !== "")
		fetchProductDetail(productId);
		fetchScheduleLogs(productId);
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
				<Grid item xs={12} sm={6} md={4} align="center">
					<Card elevation={3} sx={{ maxWidth: 345 }} align="left">
						<CardActionArea>
							<CardHeader action={
									<RelayControl ip={ip.ip} />
							}
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
						</CardContent>
							{/* {ip.name === "Climate" ?
								<ClimateData/>
							:<div></div>} */}
							{ip.name === "CO2" ?
								<Co2Chart/>
							:<div></div>}
							{ip.name === "Humidity" ?
								<HumidityChart/>
							:<div></div>}
							{ip.name === "Temperature" ?
								<TemperatureChart/>
							:<div></div>}
						</CardActionArea>
					</Card>
					</Grid>
				))}

			</Grid>
		<Grid container spacing={2} direction="row" justify="center" alignItems="stretch">
		<Grid item xs={12} sm={12} md={8}>
			<Grid container spacing={3}>
				<Grid item xs={12}>
						<ClimateChart />
				</Grid>
				<Grid item xs={12}>
						<AddClimate roomId={productId} roomIps={product.ip}/>
						<ClimateTable />
				</Grid>
			</Grid>
			</Grid>
			<Grid item xs={12} sm={12} md={4}>
					<Grid style={{ display: 'flex', height: '100%',}}>
						<ClimateLogs />
					</Grid>
				</Grid>
			</Grid>
		<Grid container spacing={2} direction="row" justify="center" alignItems="stretch">
		<Grid item xs={12} sm={12} md={8}>
			<Grid container spacing={3}>
				<Grid item xs={12}>
						<AddSchedule roomId={productId}/>
						<ScheduleTable />
				</Grid>
				<Grid item xs={12}>
						<AddInterval roomId={productId}/>
						<IntervalTable />
				</Grid>
			</Grid>
			</Grid>
			<Grid item xs={12} sm={12} md={4}>
					<Grid style={{ display: 'flex', height: '100%',}}>
						<ScheduleLogs/>
					</Grid>
				</Grid>
			</Grid>
			</Stack>
			)}
			</Container>
	);
};

export default ProductDetails;