import React from 'react';
import ReactDOM from 'react-dom/client';
import axios from "axios";
import App from './App';
import './styles/global.css';

axios.defaults.withCredentials = true;
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <App />
);

