import React from "react";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import DeleteRoom from "./DeleteRoom";
import AddIP from "./AddIP";
import DeleteIP from "./DeleteIP";
import { Form, Button, Card, ListGroup, Container, Row, Col} from 'react-bootstrap';

const ProductComponent = () => {
	const products = useSelector((state) => state.allProducts.products);
	const ips = useSelector((state) => state.allIPS.ips);

	const renderList = products.map((product,index) => {
	console.log(product.name)
		return (
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
						</ListGroup>
						<ListGroup variant="flush">
							{product.ip.map((ip,ipIndex) => (
							<ListGroup variant="flush">
								<ListGroup.Item key={ip.id}>{ip.id}</ListGroup.Item>
								<ListGroup.Item key={ip.name}>{ip.name}</ListGroup.Item>
								<ListGroup.Item key={ip.state}>{ip.state}</ListGroup.Item>
								<ListGroup.Item key={ip.ip}>{ip.ip}</ListGroup.Item>
								<ListGroup.Item>
									<DeleteIP ipId={ip.id} indexId={ipIndex} roomId={product.id} roomIndex={index}/>
								</ListGroup.Item>
							</ListGroup>
							))}
						</ListGroup>
						<ListGroup variant="flush">
						</ListGroup>
						<Link to={`/room/${product.id}`}>
							<Button variant="primary">Go somewhere</Button>
						</Link>
							<DeleteRoom roomId={product.id} indexId={index}/>
					</Card.Body>
				</Card>
			</Col>
		);
	});
	const ipList = ips.map((ipData,index) => {
		const { id, name, ip, category } = ipData;
		return (
			<Col>
				<Card
					bg={name.toLowerCase()}
					key={id}
					text={name.toLowerCase() === 'light' ? 'dark' : 'white'}
					style={{ width: '18rem' }}
					className="mb-2"
				>
				<Card.Body>
					<Card.Header style={{ color: 'black' }}>{name}</Card.Header>
					<ListGroup variant="flush">
						<ListGroup.Item key={id}>{id}</ListGroup.Item>
						<ListGroup.Item key={name}>{name}</ListGroup.Item>
						<ListGroup.Item key={ip}>{ip}</ListGroup.Item>
					</ListGroup>
					<ListGroup variant="flush">
					</ListGroup>
					<AddIP ipId={id} indexId={index}/>
				</Card.Body>
			</Card>
		</Col>
		);
	});
	return(
		<Container>
			<Row>
				<>{renderList}</>
			</Row>
			<Row>
				<>{ipList}</>
			</Row>
			</Container>
			);
};

export default ProductComponent;
{/* <Container>
	<Row>
		<Card>
			<Form onSubmit={this.handleRoom}>
				<Form.Group className="mb-3" controlId="formBasicEmail">
					<Form.Label>Create A Room</Form.Label>
					<Form.Control type="text" value={this.state.value} onChange={this.handleChange} />
					<Form.Text className="text-muted">
						Witness
					</Form.Text>
				</Form.Group>
				<Button variant="primary" type="submit">
					Create
				</Button>
			</Form>
		</Card>
	</Row>
</Container> */}