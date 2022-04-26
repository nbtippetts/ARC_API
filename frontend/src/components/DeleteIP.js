/* eslint-disable array-callback-return */
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { setIP, removeSelectedProduct, removeSelectedIPProduct } from "../redux/actions/productsActions";
import axios from "axios";
import IconButton from '@mui/material/IconButton';
import DeleteOutlined from '@mui/icons-material/DeleteOutlined';



const DeleteIP = (props) => {
	const products = useSelector((state) => state.allProducts.products);
	const ips = useSelector((state) => state.allIPS.ips);
	const id = props.ipId;
	const ipIndexId = props.indexId;
	const roomId = props.roomId;
	const roomIndex = props.index;
	const dispatch = useDispatch();

	let onDeleteClick = async (id) => {
		const response = await axios
		.delete("http://localhost:5000/room/"+roomId+"/ip/"+id)
		.catch((err) => {
			console.log("Err: ", err);
		});
		console.log(response);
		if (response.status === 204) {
			dispatch(removeSelectedProduct());
			products.map(product => {
				if(product.id===roomId){
					product.ip.map((currentIp,index) => {
						if(currentIp.id===id){
							ips.push(currentIp)
							product.ip.splice(index,1)
						}
					})
				}
			})
			console.log(products)
			dispatch(removeSelectedIPProduct(products));
			dispatch(setIP(ips));
		}
	};

	return(
	<IconButton variant="danger" key={id} onClick={()=>onDeleteClick(id)}><DeleteOutlined/></IconButton>
	);
};

export default DeleteIP;