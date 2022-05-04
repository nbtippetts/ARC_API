import { ActionTypes } from "../constants/action-types";

export const setScheduleLogs = (logs) => {
  return {
    type: ActionTypes.SET_SCHEDULE_LOGS,
    payload: logs,
  };
};
export const setClimateLogs = (logs) => {
  return {
    type: ActionTypes.SET_CLIMATE_LOGS,
    payload: logs,
  };
};
export const setChartLogs = (logs) => {
  return {
    type: ActionTypes.SET_CHART_LOGS,
    payload: logs,
  };
};

export const resetLogs = (logs) => {
  return {
    type: ActionTypes.RESET_LOGS,
  };
};