import { combineReducers } from "redux";
import { addProductReducer, productsReducer, selectedProductsReducer, ipsReducer, selectedIPSReducer} from "./productsReducer";
const reducers = combineReducers({
  allProducts: productsReducer,
  product: selectedProductsReducer,
  addProduct: addProductReducer,
  allIPS: ipsReducer,
  ip: selectedIPSReducer,
});
export default reducers;
