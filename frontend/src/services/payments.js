import api from "config/axios";

const createPayment = async (payload) => {
  return api.post("/payments/", payload);
};

export { createPayment };
