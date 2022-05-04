import { ActionTypes } from "../constants/action-types";
const intialState = {
  climateLogs: [],
  scheduleLogs: [],
  chartLogs: [],
};

export const scheduleLogsReducer = (state = intialState, { type, payload }) => {
  switch (type) {
    case ActionTypes.SET_SCHEDULE_LOGS:
      return { ...state, scheduleLogs: payload };
    default:
      return state;
  }
};
export const climateLogsReducer = (state = intialState, { type, payload }) => {
  switch (type) {
    case ActionTypes.SET_CLIMATE_LOGS:
      return { ...state, climateLogs: payload };
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

export const resetLogsReducer = (state = intialState, { type, payload }) => {
  console.log(type);
  switch (type) {
    case ActionTypes.RESET_LOGS:
      return state
    default:
      return state;
  }
};