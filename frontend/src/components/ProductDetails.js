import React, { useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Box,Stack, Card, CardActionArea, CardContent, Container,Typography,Grid} from '@mui/material';
import {
	selectedProduct,
	removeSelectedProduct
} from "../redux/actions/productsActions";
import AddSchedule from "./AddSchedule";
import ScheduleTable from "./ScheduleTable";

const ProductDetails = () => {
	const { productId } = useParams();
	let product = useSelector((state) => state.product);
	const dispatch = useDispatch();
	const fetchProductDetail = async (id) => {
		const response = await axios
			.get(`http://localhost:5000/room/${id}`)
			.catch((err) => {
				console.log("Err: ", err);
			});
		dispatch(selectedProduct(response.data));
	};

	useEffect(() => {
		if (productId && productId !== "")
		fetchProductDetail(productId);
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
				<Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
				{product.ip.map((ip,ipIndex) => (
					<Grid item xs={2} sm={4} md={4} key={ipIndex}>
					<Card sx={{ maxWidth: 345 }}>
						<CardActionArea>
						<CardContent>
							<Typography
								className={"MuiTypography--heading"}
								variant={"h6"}
								gutterBottom>{ip.name}</Typography>
							<Typography
								className={"MuiTypography--subheading"}
								 variant={"caption"}>{ip.id}
							</Typography>
							<Typography
								className={"MuiTypography--subheading"}
								 variant={"caption"}>{ip.state}
							</Typography>
							<Typography
								className={"MuiTypography--subheading"}
								 variant={"caption"}>{ip.ip}
							</Typography>

						</CardContent>
						</CardActionArea>
					</Card>
					</Grid>
				))}
			</Grid>
			<Box>
				<AddSchedule roomId={productId}/>
				<ScheduleTable />
			</Box>
			</Stack>
			)}
			</Container>
	);
};

export default ProductDetails;