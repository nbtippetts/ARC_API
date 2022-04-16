import React, { Component, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setProducts } from "../redux/actions/productsActions";
import axios from "axios";
import { Form, Button, Card, ListGroup, Container, Row, Col} from 'react-bootstrap';



const AddRoom = () => {
const [room_name, setName] = useState("");
const products = useSelector((state) => state.allProducts.products);
const room_id = products.length+1;
const dispatch = useDispatch();

	let handleSubmit = async (e) => {
		e.preventDefault();
		const response = await axios
      .put("http://localhost:5000/room/"+room_id,{name:room_name})
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
				<Container>
					<Row>
						<Form onSubmit={handleSubmit}>
							<Form.Group className="mb-3" controlId="formGroupEmail">
									<Form.Label>Create A Room</Form.Label>
									<Form.Control type="text" onChange={(e) => setName(e.target.value)} placeholder="Create A Room" />
								</Form.Group>
								<Button variant="primary" type="submit">ADD</Button>
						</Form>
					</Row>
				</Container>
			);
};

export default AddRoom;