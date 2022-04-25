import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setIPProducts, removeSelectedIP } from "../redux/actions/productsActions";
import axios from "axios";
import { Form} from 'react-bootstrap';
import Stack from '@mui/material/Stack';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';


const AddIP = (props) => {
	const [focusItemId, setFocusItemId] = useState(-1);
	const [roomId, setRoomId] = useState("");
	const [roomIndexId, setRoomIndexId] = useState("");
	const products = useSelector((state) => state.allProducts.products);
	const id = props.ipId;
	const ipIndexId = props.indexId;
	const dispatch = useDispatch();

	let handleSubmit = async (e) => {
		e.preventDefault();
		const response = await axios
		.patch("http://localhost:5000/room/"+roomId+"/ip/"+id)
		.catch((err) => {
			console.log("Err: ", err);
		});
		console.log(response);
		if (response.status === 201) {
			dispatch(removeSelectedIP(ipIndexId));
			products.map((product,index) => {
				if(product.id==roomId){
					product.ip.push(response.data)
				}
			})
			console.log(products)
			dispatch(setIPProducts(products));
		}
	};
	const handleSelect=(key,value)=>{
		setRoomIndexId(key);
		setRoomId(value);
		setFocusItemId(focusItemId === key ? -1 : key);
  	}
	return(
			<Form onSubmit={handleSubmit}>
				<Stack direction="row" spacing={2}>
					{products.map((product,index) => (
						<MenuItem selected={focusItemId === index} onClick={() => handleSelect(index,product.id)} value={product.name}>{product.name}</MenuItem>
					))}
				<Button variant="primary" type="submit">ADD</Button>
				</Stack>
			</Form>
	);
};

export default AddIP;