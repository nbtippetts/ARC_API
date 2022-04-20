import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { Provider } from 'react-redux'
import store from './redux/store'
import reportWebVitals from "./reportWebVitals";
import 'bootstrap/dist/css/bootstrap.min.css';
import { ThemeProvider, createTheme } from '@mui/material/styles';
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
  typography: {
	  fontFamily: 'Baloo'
  }
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <ThemeProvider theme={darkTheme}>
    <Provider store={store}>
      <App />
    </Provider>
  </ThemeProvider>
);

reportWebVitals();
