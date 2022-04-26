import React from "react";
import ReactDOM from 'react-dom';
import "./index.css";
import App from "./App";
import { Provider } from 'react-redux'
import store from './redux/store'
import reportWebVitals from "./reportWebVitals";
import { ThemeProvider, createTheme } from '@mui/material/styles';
const darkTheme = createTheme({
  palette: {
    primary: {
      light: '#757ce8',
      main: '#3f50b5',
      dark: '#002884',
      contrastText: '#fff',
    },
    secondary: {
      light: '#ff7961',
      main: '#f44336',
      dark: '#ba000d',
      contrastText: '#000',
    },
  },
  typography: {
	  fontFamily: 'Helvetica Neue'
  }
});


ReactDOM.render(
  <ThemeProvider theme={darkTheme}>
    <Provider store={store}>
      <App />
    </Provider>
  </ThemeProvider>,
  document.getElementById('root')
);

reportWebVitals();
