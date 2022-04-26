import { ActionTypes } from "../constants/action-types";

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

export const resetLogs = () => {
  return {
    type: ActionTypes.RESET_LOGS,
  };
};