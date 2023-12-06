import axios from "axios";

const { REACT_APP_SERVER_PORT } = process.env;
console.log("REACT_APP_SERVER_PORT", REACT_APP_SERVER_PORT);

export const instance = axios.create({
  baseURL: `http://${process.env.REACT_APP_SERVER_PORT}`,
  withCredentials: true,
  timeout: 600000,
  headers: {
    "Content-Type": "application/json",
  },
});