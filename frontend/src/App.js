import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Routes
} from "react-router-dom";
import axios from 'axios'

import ProductListing from './components/ProductListing';
import ProductDetails from './components/ProductDetails';
import AddRoom from './components/AddRoom';
import DeleteRoom from './components/DeleteRoom';



function App() {
	return (
		<Router>
					<Routes>
						<Route path='/' element={<><AddRoom /><ProductListing /></>}/>
              			<Route path="/room/:productId" element={<ProductDetails />} />
					</Routes>
		</Router>


	);

}

export default App;