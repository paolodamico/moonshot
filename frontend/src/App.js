import React from "react";
import NavigationProvider from "components/providers/Navigation";
import { loadStripe } from "@stripe/stripe-js";
import { Elements } from "@stripe/react-stripe-js";
import { STRIPE_PUBLIC_KEY } from "constants.js";

const stripePromise = loadStripe(STRIPE_PUBLIC_KEY);

function App() {
  return (
    <Elements stripe={stripePromise}>
      <NavigationProvider />
    </Elements>
  );
}

export default App;
