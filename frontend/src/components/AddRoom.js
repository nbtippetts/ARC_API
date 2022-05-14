import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setProducts } from "../redux/actions/productsActions";
import axios from "axios";
import { Card,Grid,TextField,CardHeader,CardContent} from '@mui/material';
import IconButton from '@mui/material/IconButton';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import AddCircleIcon from '@mui/icons-material/AddCircle';



const AddRoom = () => {
const [room_name, setName] = useState("");
const products = useSelector((state) => state.allProducts.products);
const room_id = products.length+1;
const dispatch = useDispatch();

	let handleSubmit = async (e) => {
		const response = await axios
			.put("/room/"+room_id,{name:room_name})
			.catch((err) => {
				console.log("Err: ", err);
			});
			console.log(response);
			if (response.status === 201) {
				setName("")
				dispatch(setProducts([...products, response.data]));
			}
		};

			return (
				<Grid container spacing={2}>
					<Grid item xs={12} sm={6} md={4}>
					<Card elevation={1}>
							<CardHeader
							action = {
								<HomeRoundedIcon/>
							}
							title="Create Your Environment"
							>
							</CardHeader>

							<CardContent>
							<form onSubmit={handleSubmit}>
								<TextField style={{width: "80%"}} id="standard-basic" label="Create A Room" variant="standard" placeholder="Create A Room" onChange={e => setName(e.target.value)} />
								<IconButton variant="primary" type="submit"><AddCircleIcon/></IconButton>
							</form>
							</CardContent>
						</Card>
					</Grid>
				</Grid>
			);
};

export default AddRoom;