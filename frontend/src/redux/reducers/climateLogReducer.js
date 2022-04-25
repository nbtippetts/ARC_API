import { Action } from "history";
import { ActionTypes } from "../constants/action-types";
const intialState = {
  logs: [],
  chartLogs: [],
};

export const logsReducer = (state = intialState, { type, payload }) => {
  switch (type) {
    case ActionTypes.SET_LOGS:
      return { ...state, logs: payload };
    default:
      return state;
  }
};
export const chartLogsReducer = (state = intialState, { type, payload }) => {
  switch (type) {
    case ActionTypes.SET_CHART_LOGS:
      return { ...state, chartLogs: payload };
    default:
      return state;
  }
};