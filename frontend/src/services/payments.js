import api from "config/axios";

const createPayment = async (payload) => {
  return api.post("/payments/", payload);
};

const fetchPayments = async () => {
  return api.get("/payments/");
};

export { createPayment, fetchPayments };
