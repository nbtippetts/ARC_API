import { ActionTypes } from "../constants/action-types";

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
export const setSchedules = (product) => {
  return {
    type: ActionTypes.SET_SCHEDULE,
    payload: product,
  };
};
export const removeSchedule = (index) => {
  return {
    type: ActionTypes.REMOVE_SELECTED_SCHEDULE,
    payload: index,
  };
};

export const setIntervals = (product) => {
  return {
    type: ActionTypes.SET_INTERVAL,
    payload: product,
  };
};
export const removeInterval = (index) => {
  return {
    type: ActionTypes.REMOVE_SELECTED_INTERVAL,
    payload: index,
  };
};
export const setClimates = (product) => {
  return {
    type: ActionTypes.SET_CLIMATE,
    payload: product,
  };
};
export const removeClimate = (index) => {
  return {
    type: ActionTypes.REMOVE_SELECTED_CLIMATE,
    payload: index,
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