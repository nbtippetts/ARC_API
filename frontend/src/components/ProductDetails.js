import React, { useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Form, Button, Card, ListGroup, Container, Row, Col} from 'react-bootstrap';
import {
	selectedProduct,
	removeSelectedProduct,
} from "../redux/actions/productsActions";
const ProductDetails = () => {
	const { productId } = useParams();
	let product = useSelector((state) => state.product);
	const { name, title, price, category, description } = product;
	const dispatch = useDispatch();
	const fetchProductDetail = async (id) => {
		const response = await axios
			.get(`http://localhost:5000/room/${id}`)
			.catch((err) => {
				console.log("Err: ", err);
			});
		dispatch(selectedProduct(response.data));
	};
		let onDeleteClick = async (id) => {
			console.log(id)
			const response = await axios
				.delete("http://localhost:5000/room/"+id)
				.catch((err) => {
					console.log("Err: ", err);
					});
					console.log(response);
					if (response.status === 201) {
						dispatch(removeSelectedProduct(id));
					}
		}

	useEffect(() => {
		if (productId && productId !== "") fetchProductDetail(productId);
		return () => {
			dispatch(removeSelectedProduct());
		};
	}, [productId]);
	return (
		<div className="ui grid container">
			{Object.keys(product).length === 0 ? (
				<div>...Loading</div>
			) : (
				<Col>
					<Card
						bg={product.name.toLowerCase()}
						key={product.id}
						text={product.name.toLowerCase() === 'light' ? 'dark' : 'white'}
						style={{ width: '18rem' }}
						className="mb-2"
					>
						<Card.Body>
							<Card.Header style={{ color: 'black' }}>{product.name}</Card.Header>
							<ListGroup variant="flush">
								<ListGroup.Item key={product.id}>{product.id}</ListGroup.Item>
								<ListGroup.Item key={product.name}>{product.name}</ListGroup.Item>
								<ListGroup.Item key={product.climate}>{product.climate}</ListGroup.Item>


							</ListGroup>
							<ListGroup variant="flush">

							</ListGroup>
							<Button variant="danger" onClick={()=>onDeleteClick(product.id)}>Delete</Button>

						</Card.Body>
					</Card>
					</Col>
			)}
		</div>
	);
};

export default ProductDetails;