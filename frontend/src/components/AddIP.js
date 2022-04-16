import React, { Component, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setIPProducts,setProducts, removeSelectedIP } from "../redux/actions/productsActions";
import axios from "axios";
import { Form, Button,DropdownButton, Dropdown, Container, Row, Col} from 'react-bootstrap';



const AddIP = (props) => {
	const [roomId, setRoomId] = useState("");
	const [roomIndexId, setRoomIndexId] = useState("");
	const products = useSelector((state) => state.allProducts.products);
	const ips = useSelector((state) => state.allIPS.ips);
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
	const handleSelect=(e)=>{
		console.log(e)
		const indexArr = e.split(",");
		setRoomId(indexArr[0]);
		setRoomIndexId(indexArr[1]);
  	}
	return(
	<Container>
		<Row>
			<Form onSubmit={handleSubmit}>
				<Form.Group className="mb-3" controlId="formGroupEmail">
					<DropdownButton
						title="Add To Room"
						id="dropdown-menu-align-right"
						onSelect={handleSelect}>
							{products.map((product,index) => (
								<Dropdown.Item eventKey={[product.id,index]}>{product.name}</Dropdown.Item>
							))}
					</DropdownButton>
				</Form.Group>
				<Button variant="primary" type="submit">ADD</Button>
			</Form>
		</Row>
	</Container>
	);
};

export default AddIP;