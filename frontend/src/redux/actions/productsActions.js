import { ActionTypes } from "../constants/action-types";
import axios from "axios";

export const setProducts = (products) => {
  return {
    type: ActionTypes.SET_PRODUCTS,
    payload: products,
  };
};
export const setIPProducts = (products) => {
  return {
    type: ActionTypes.SET_IP_PRODUCT,
    payload: products,
  };
};
export const setIP = (index) => {
  return {
    type: ActionTypes.SET_IP,
    payload: index,
  };
};

export const selectedProduct = (product) => {
  return {
    type: ActionTypes.SELECTED_PRODUCT,
    payload: product,
  };
};
export const removeSelectedProduct = (index) => {
  return {
    type: ActionTypes.REMOVE_SELECTED_PRODUCT,
    payload: index,
  };
};
export const setIPS = (ips) => {
  return {
    type: ActionTypes.SET_IPS,
    payload: ips,
  };
};

export const selectedIP = (ip) => {
  return {
    type: ActionTypes.SELECTED_IP,
    payload: ip,
  };
};
export const removeSelectedIP = (index) => {
  return {
    type: ActionTypes.REMOVE_SELECTED_IP,
    payload: index,
  };
};
export const removeSelectedIPProduct = (index) => {
  return {
    type: ActionTypes.REMOVE_SELECTED_IP_PRODUCT,
    payload: index,
  };
};