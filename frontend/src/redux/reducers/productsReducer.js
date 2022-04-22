import { Action } from "history";
import { ActionTypes } from "../constants/action-types";
const intialState = {
  products: [],
  product: {
    climate: [],
    climate_schedule:[],
    climate_interval:[],
    IP:[]
  },
  ips: [],
};

export const addProductReducer = (state = intialState, { type, payload }) => {
  console.log(type);
  switch (type) {
    case ActionTypes.ADD_PRODUCTS:
      return { ...state, ...payload };
    default:
      return state;
  }
};
export const productsReducer = (state = intialState, { type, payload }) => {
  switch (type) {
    case ActionTypes.SET_PRODUCTS:
      return { ...state, products: payload };

    case ActionTypes.SET_IP_PRODUCT:
      console.log(payload)
      return { ...state,payload };

    case ActionTypes.REMOVE_SELECTED_IP_PRODUCT:
      console.log(payload)
      return { ...state, payload };

    case ActionTypes.REMOVE_SELECTED_PRODUCT:
      console.log(payload)
      return { ...state, products: state.products.filter((product,index) => index !== payload) };

    default:
      return state;
  }
};

export const selectedProductsReducer = (state = {}, { type, payload }) => {
  console.log(type);
  switch (type) {
    case ActionTypes.SELECTED_PRODUCT:
      return { ...state,...payload}
    case ActionTypes.SET_SCHEDULE:
      return { ...state, payload };
    case ActionTypes.REMOVE_SELECTED_SCHEDULE:
      return { ...state, payload };
    case ActionTypes.SET_INTERVAL:
      return { ...state, payload };
    case ActionTypes.REMOVE_SELECTED_INTERVAL:
      return { ...state, payload };
    case ActionTypes.SET_CLIMATE:
      return { ...state, payload };
    case ActionTypes.REMOVE_SELECTED_CLIMATE:
      return { ...state, payload };
    default:
      return state;
  }
};
export const ipsReducer = (state = intialState, { type, payload }) => {
  switch (type) {
    case ActionTypes.SET_IPS:
      return { ...state, ips: payload };

    case ActionTypes.SET_IP:
      console.log(payload)
      return { ...state,payload };

    case ActionTypes.REMOVE_SELECTED_IP:
      console.log(payload)
      return { ...state, ips: state.ips.filter((ip,index) => index !== payload) };

    default:
      return state;
  }
};

export const selectedIPSReducer = (state = {}, { type, payload }) => {
  console.log(type);
  switch (type) {
    case ActionTypes.SELECTED_IP:
      return { ...state, ...payload };
    default:
      return state;
  }
};
