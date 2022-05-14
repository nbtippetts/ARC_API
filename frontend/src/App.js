// import './App.css';
import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Routes
} from "react-router-dom";

import ProductListing from './components/ProductListing';
import ProductDetails from './components/ProductDetails';

function App() {
	return (
			<Router>
					<Routes>
						<Route path='/' element={<ProductListing />}/>
              			<Route path="/room/:productId" element={<ProductDetails />} />
					</Routes>
			</Router>
	);

}

export default App;