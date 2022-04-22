import { Action } from "history";
import { ActionTypes } from "../constants/action-types";
const intialState = {
  logs: [],
};

export const logsReducer = (state = intialState, { type, payload }) => {
  switch (type) {
    case ActionTypes.SET_LOGS:
      return { ...state, logs: payload };
    default:
      return state;
  }
};