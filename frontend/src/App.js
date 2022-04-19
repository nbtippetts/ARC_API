import logo from './logo.svg';
import './App.css';
import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Routes
} from "react-router-dom";

import ProductListing from './components/ProductListing';
import ProductDetails from './components/ProductDetails';
import AddRoom from './components/AddRoom';
import { ThemeProvider, createTheme } from '@mui/material/styles';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
  typography: {
	  fontFamily: 'Baloo'
  }
});

function App() {
	return (
		<ThemeProvider theme={darkTheme}>
			<Router>
					<Routes>
						<Route path='/' element={<><AddRoom /><ProductListing /></>}/>
              			<Route path="/room/:productId" element={<ProductDetails />} />
					</Routes>
			</Router>
		</ThemeProvider>


	);

}

export default App;