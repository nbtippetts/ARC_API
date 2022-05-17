// import './App.css';
import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Routes
} from "react-router-dom";

import ProductListing from './components/ProductListing';
import ProductDetails from './components/ProductDetails';
import { Network } from './components/Network';

function App() {
	return (
			<Router>
					<Routes>
						<Route path='/' element={<ProductListing />}/>
              			<Route path="/room/:productId" element={<ProductDetails />} />
              			<Route path="/network" element={<Network />} />
					</Routes>
			</Router>
	);

}

export default App;