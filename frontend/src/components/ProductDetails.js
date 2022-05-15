import React, { useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Avatar, Stack, Card, CardHeader, CardActionArea, CardContent, Grid} from '@mui/material';
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
import { setNotes } from "../redux/actions/NoteBookActions";
import AddInterval from "./AddInterval";
import AddSchedule from "./AddSchedule";
import IntervalTable from "./IntervalTable";
import ScheduleTable from "./ScheduleTable";
import { ClimateChart } from "./ClimateChart";
import { ScheduleLogs } from "./ScheduleLogs";
import { Co2Chart } from "./Co2Chart";
import { HumidityChart } from "./HumidityChart";
import { TemperatureChart } from "./TemperatureChart";
import { VpdChart } from "./VpdChart";
import { ClimateData } from "./ClimateData";
import AddClimate from "./AddClimate";
import ClimateTable from "./ClimateTable";
import { ClimateLogs } from "./ClimateLogs";
import { RelayControl } from "./RelayControl";
import NoteBook from "./NoteBook";
import { makeStyles } from "@mui/styles";

const useStyles = makeStyles(theme => ({
  overviewcard: {
	height: "100%",
    display:"flex",
	flexDirection: "column",
		"&.MuiDataGrid-root .MuiPaper-root-MuiCard-root": {
			transition: "box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms",
			backgroundImage: "linear-gradient(rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.05))",
			overflow: "hidden",
			borderRadius: "20px",
			boxShadow: "rgb(90 114 123 / 11%) 0px 7px 30px 0px",
			backgroundColor: "rgb(251, 150, 120)",
			color: "white",
		},
	},
}));

const ProductDetails = () => {
	const { productId } = useParams();
	let product = useSelector((state) => state.product);
	const dispatch = useDispatch();
	const classes = useStyles();
	useEffect(() => {
		const fetchProductDetail = async (id) => {
			const response = await axios
				.get(`/room/${id}`)
				.catch((err) => {
					console.log("Err: ", err);
				});
			dispatch(selectedProduct(response.data));
		};
		const fetchClimateLogs = async (id) => {
			const response = await axios
			.get(`/room/${id}/ip_chart_logs`)
			.catch((err) => {
				console.log("Err: ", err);
			});
			if (response.status === 200) {
				let shtClimateLogs = response.data.climate_log[0]
				let displayLogs = response.data.climate_log[0].slice(0,20)
				const removeElemWithIdAndValue = (arr = []) => {
					// eslint-disable-next-line array-callback-return
					arr.map(value => {
						if (value.co2 === 0) {
							delete value['co2']
						}
					})
				}
				// removeElemWithIdAndValue(shtClimateLogs, 'co2', 0);
				dispatch(setClimateLogs(shtClimateLogs));
				removeElemWithIdAndValue(displayLogs, 'co2', 0);
				dispatch(setChartLogs(displayLogs.reverse()));
			} else {
				dispatch(setClimateLogs([]));
				dispatch(setChartLogs([]));
			}
		}
		const fetchNotes = async (id) => {
			const response = await axios
			.get(`/room/${id}/note/1`)
			.catch((err) => {
				console.log("Err: ", err);
			});
			if (response.status === 200) {
				dispatch(setNotes(response.data));
			}  else {
				dispatch(setNotes([]));
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
			} else {
				dispatch(setScheduleLogs([]));

			}
		}
		if (productId && productId !== "")
		fetchProductDetail(productId);
		fetchScheduleLogs(productId);
		fetchClimateLogs(productId);
		fetchNotes(productId);
		return () => {
			dispatch(removeSelectedProduct());
		};
	}, [productId]);

	return (

		<Stack spacing={2}>
			{Object.keys(product).length === 0 ? (
				<div>...Loading</div>
			) : (
		<Grid container spacing={2} direction="row" justify="center" alignItems="stretch">
			<Grid item xs={12} sm={4} md={4}>
			<Grid container spacing={2} style={{ display: 'flex', flexWrap: 'wrap', padding: "10px"}}>
				{product.ip.map((ip,ipIndex) => (
				<Grid item xs={12} sm={12} md={12} lg={6}>
					<Card elevation={3} sx={{ maxWidth: 275}} align="center" style={{borderRadius:"20px"}} className={classes.overviewcard}>
						<CardActionArea>
							<CardHeader
								action={
									<RelayControl ip={ip.ip} />
								}
								avatar={
									<Avatar>
										{ip.name === "Climate" ? <CloudIcon/> :
										ip.name === "Temperature" ? <ThermostatIcon/> :
										ip.name === "Humidity" ? <OpacityIcon/> :
										ip.name === "CO2" ? <Co2Icon/> :
										ip.name === "Water" ? <ShowerIcon/> :
										ip.name === "Light" ? <LightbulbIcon/> : <QuestionMarkIcon/>}
									</Avatar>
								}
								subheader={ip.name}
								>
							</CardHeader>
							 {/* {ip.state.toString()} */}
							{ip.name === "Climate" ?
							<div>
								<ClimateData ipId={ip.id}/>
								<VpdChart/>
							</div>
							:<div></div>}
							{ip.name === "CO2" ?
								<div>
									<CardContent></CardContent>
									<Co2Chart/>
								</div>
								:<div></div>}
							{ip.name === "Humidity" ?
								<div>
									<CardContent></CardContent>
									<HumidityChart/>
								</div>
								:<div></div>}
							{ip.name === "Temperature" ?
								<div>
									<CardContent></CardContent>
									<TemperatureChart/>
								</div>
							:<div></div>}
						</CardActionArea>
					</Card>
					</Grid>
				))}
					</Grid>
				</Grid>
		<Grid item xs={12} sm={8} md={8}>
			<Grid container spacing={2}>
				<Grid item xs={12}>
					<Card elevation={3} align="center" style={{borderRadius:"20px"}}>
						<CardContent>
							<ClimateChart />
						</CardContent>
					</Card>
				</Grid>
				<Grid item xs={12}>
						<AddClimate roomId={productId} roomIps={product.ip}/>
						<ClimateTable />
				</Grid>
				<Grid item xs={12}>
					<Stack spacing={2}>
						<AddSchedule roomId={productId}/>
						<ScheduleTable />

						<AddInterval roomId={productId}/>
						<IntervalTable />
					</Stack>
				</Grid>
			</Grid>
			</Grid>
			</Grid>
			)}
			<Grid container spacing={2} direction="row" justify="center" alignItems="stretch" style={{paddingRight:"16px"}}>
				<Grid item xs={12} sm={6} md={6}>
					<Stack spacing={2}>
						<ClimateLogs />
						<ScheduleLogs/>
					</Stack>
				</Grid>
				<Grid item xs={12} sm={6} md={6}>
					<NoteBook roomId={productId}/>
				</Grid>
			</Grid>
			</Stack>
	);
};

export default ProductDetails;