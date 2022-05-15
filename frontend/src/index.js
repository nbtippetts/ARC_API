import React from "react";
import ReactDOM from 'react-dom';
import "./index.css"
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
  },
  components: {
    // Name of the component
    MuiDataGrid: {
      styleOverrides: {
        // Name of the slot
        root: {
          // Some CSS
          padding: '10px',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        // Name of the slot
        root: {
          color: "black"
        },
      },
    },
    MuiDialogTitle: {
      styleOverrides: {
        // Name of the slot
        root: {
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        },
      },
    },
    // MuiButton: {
    //   styleOverrides: {
    //     // Name of the slot
    //     root: {
    //       display: "inline-flex",
    //       alignItems: "center",
    //       justifyContent: "center",
    //       position: "relative",
    //       boxSizing: "border-box",
    //       outline: "0px",
    //       border: "0px",
    //       margin: "15px 0px 0px",
    //       cursor: "pointer",
    //       userSelect: "none",
    //       verticalAlign: "middle",
    //       appearance: "none",
    //       textDecoration: "none",
    //       fontWeight: "400",
    //       lineHeight: "1.75",
    //       minWidth: "64px",
    //       padding: "6px 16px",
    //       borderRadius: "5px",
    //       transition: "all 0.3s ease 0s",
    //       color: "rgb(255, 255, 255)",
    //       backgroundColor: "rgb(3, 201, 215)",
    //       textTransform: "none",
    //       boxShadow: "none",
    //       fontSize: "15px",
    //       '&:hover': {
    //           backgroundColor: 'red',
    //           color: '#3c52b2',
    //       },
    //     },
    //   },
    // },
  },
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
