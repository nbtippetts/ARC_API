import React, { useEffect, useCallback, useMemo } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { setProducts, setIPS, removeSelectedProduct } from "../redux/actions/productsActions";
import ProductComponent from "./ProductComponent";

const ProductPage = () => {
  const products = useSelector((state) => state.allProducts.products);
  const ips = useSelector((state) => state.allIPS.ips);
  const dispatch = useDispatch();
  const fetchProducts = async () => {
    const response = await axios
      .get("http://localhost:5000/rooms")
      .catch((err) => {
        console.log("Err: ", err);
      });
      console.log(response)
      if(response != null){
        dispatch(setProducts(response.data));
      }
  };
  const fetchIPS = async () => {
    const response = await axios
      .get("http://localhost:5000/all_ips")
      .catch((err) => {
        console.log("Err: ", err);
      });
       if(response != null){
         dispatch(setIPS(response.data));
       }
  };


  useEffect(() => {
    fetchProducts();
    fetchIPS();
  }, []);

  console.log("Products :", products);
  console.log("IPS :", ips);
  return (
    <div className="ui grid container">
      <ProductComponent />
    </div>
  );
};

export default ProductPage;