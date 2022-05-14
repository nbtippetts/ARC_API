/* eslint-disable react-hooks/exhaustive-deps */
import React, { useEffect } from "react";
import axios from "axios";
import { useDispatch } from "react-redux";
import { setProducts, setIPS } from "../redux/actions/productsActions";
import ProductComponent from "./ProductComponent";

const ProductPage = () => {
  const dispatch = useDispatch();
  const fetchProducts = async () => {
    const response = await axios
      .get("/rooms")
      .catch((err) => {
        console.log("Err: ", err);
      });
      if(response != null){
        const productData = response.data;
        dispatch(setProducts(productData));
      }
  };
  const fetchIPS = async () => {
    const response = await axios
      .get("/all_ips")
      .catch((err) => {
        console.log("Err: ", err);
      });
       if(response != null){
         const ipData = response.data;
         dispatch(setIPS(ipData));
       }
  };


  useEffect(() => {
    fetchProducts();
    fetchIPS();
  }, []);

  return (
      <ProductComponent />
  );
};

export default ProductPage;