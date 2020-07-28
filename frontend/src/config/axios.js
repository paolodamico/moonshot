import axios from "axios";
import { toaster } from "evergreen-ui";
import { API_URL } from "constants.js";

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: { "Content-Type": "application/json" },
});

const pass = (response) => response;

const handleError = (error) => {
  toaster.danger(
    "Something wrong happened! Please check the logs or try again."
  );
  const response = error.response || { status: -1, data: null };
  return Promise.resolve(response);
};

const setInterceptors = (instance) => {
  instance.interceptors.response.use(pass, handleError);
};

setInterceptors(api);

export default api;
