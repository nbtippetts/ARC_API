import { ActionTypes } from "../constants/action-types";
import axios from "axios";

export const setLogs = (logs) => {
  return {
    type: ActionTypes.SET_LOGS,
    payload: logs,
  };
};
export const setChartLogs = (logs) => {
  return {
    type: ActionTypes.SET_CHART_LOGS,
    payload: logs,
  };
};
