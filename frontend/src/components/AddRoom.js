import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setProducts } from "../redux/actions/productsActions";
import axios from "axios";
import { Card,Grid,TextField,Button} from '@mui/material';



const AddRoom = () => {
const [room_name, setName] = useState("");
const products = useSelector((state) => state.allProducts.products);
const room_id = products.length+1;
const dispatch = useDispatch();

	let handleSubmit = async (e) => {
		e.preventDefault();
		const response = await axios
      .put("/room/"+room_id,{name:room_name})
      .catch((err) => {
        console.log("Err: ", err);
				});
				console.log(response);
				if (response.status === 201) {
					dispatch(setProducts([...products, response.data]));
					setName("")
				}
		};

			return (
				<Grid container spacing={2}>
					<Grid item xs={6}>
						<Card elevation={3} sx={{ maxWidth: 345 }}>
							<form onSubmit={handleSubmit}>
								<TextField id="standard-basic" label="Create A Room" variant="standard" placeholder="Create A Room" onChange={e => setName(e.target.value)} />
								<Button variant="primary" type="submit">ADD</Button>
							</form>
						</Card>
					</Grid>
				</Grid>
			);
};

export default AddRoom;