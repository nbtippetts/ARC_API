import React, { useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Box,Stack, Card, CardActionArea, CardContent, Container,Typography,Grid} from '@mui/material';
import {
	selectedProduct,
	removeSelectedProduct
} from "../redux/actions/productsActions";
import { setLogs } from '../redux/actions/climateLogActions';
import AddInterval from "./AddInterval";
import AddSchedule from "./AddSchedule";
import IntervalTable from "./IntervalTable";
import ScheduleTable from "./ScheduleTable";
import { Co2Chart } from "./Co2Chart";
import { HumidityChart } from "./HumidityChart";
import { TemperatureChart } from "./TemperatureChart";
import { makeStyles } from "@mui/styles";
import AddClimate from "./AddClimate";
import ClimateTable from "./ClimateTable";
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
	const logs = useSelector((state) => state.allLogs.logs);
	const dispatch = useDispatch();
	const classes = useStyles();
	const fetchProductDetail = async (id) => {
		const response = await axios
			.get(`http://localhost:5000/room/${id}`)
			.catch((err) => {
				console.log("Err: ", err);
			});
		response.data.ip.map((ips,index) =>{
			if(ips.name === "Climate"){
				response.data.ip.splice(index,1)
			}
		})
		dispatch(selectedProduct(response.data));
	};
	const fetchClimateLogs = async (id) => {
		const response = await axios
		.get(`http://localhost:5000/room/${id}/ip_logs`)
		.catch((err) => {
			console.log("Err: ", err);
		});
		if (response.status === 200) {
			dispatch(setLogs(response.data.climate_log));
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
		<Container maxWidth="lg">
			{Object.keys(product).length === 0 ? (
				<div>...Loading</div>
			) : (
				<Stack spacing={2}>
				<Grid container spacing={{ xs: 2, md: 4, lg: 6 }} columns={{ xs: 4, sm: 8, md: 12 }}>
				{product.ip.map((ip,ipIndex) => (
				<Grid item xs={12} sm={6} md={3} key={ipIndex}>
					<Card sx={{ maxWidth: 345 }}>
						<CardActionArea>
						<CardContent className={classes.overviewcard}>
							<Typography
								className={"MuiTypography--headingflex"}
								variant={"h6"}
								gutterBottom>{ip.name}
								</Typography>
							<Typography
								className={"MuiTypography--subheading"}
								 variant={"caption"}>{ip.id}
							</Typography>
							<Typography
								className={"MuiTypography--subheading"}
								 variant={"caption"}>{ip.state.toString()}
							</Typography>
							<Typography
								className={"MuiTypography--subheading"}
								 variant={"caption"}>{ip.ip}
							</Typography>
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
			<Box>
				<AddSchedule roomId={productId}/>
				<ScheduleTable />
				<AddInterval roomId={productId}/>
				<IntervalTable />
				<AddClimate roomId={productId} roomIps={product.ip}/>
				<ClimateTable />
			</Box>
			</Stack>
			)}
			</Container>
	);
};

export default ProductDetails;