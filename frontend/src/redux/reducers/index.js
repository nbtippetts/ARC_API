import { combineReducers } from "redux";
import { addProductReducer, productsReducer, selectedProductsReducer, ipsReducer, selectedIPSReducer} from "./productsReducer";
import { logsReducer,chartLogsReducer } from "./climateLogReducer";
const reducers = combineReducers({
  allProducts: productsReducer,
  product: selectedProductsReducer,
  addProduct: addProductReducer,
  allIPS: ipsReducer,
  ip: selectedIPSReducer,
  allLogs: logsReducer,
  cardLogs: chartLogsReducer
});
export default reducers;