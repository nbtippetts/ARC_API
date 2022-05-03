import { combineReducers } from "redux";
import { addProductReducer, productsReducer, selectedProductsReducer, ipsReducer, selectedIPSReducer} from "./productsReducer";
import { scheduleLogsReducer,climateLogsReducer,chartLogsReducer, resetLogsReducer } from "./climateLogReducer";
const reducers = combineReducers({
  allProducts: productsReducer,
  product: selectedProductsReducer,
  addProduct: addProductReducer,
  allIPS: ipsReducer,
  ip: selectedIPSReducer,
  allClimateLogs: climateLogsReducer,
  allScheduleLogs: scheduleLogsReducer,
  cardLogs: chartLogsReducer,
  resetLogs:resetLogsReducer
});
export default reducers;
