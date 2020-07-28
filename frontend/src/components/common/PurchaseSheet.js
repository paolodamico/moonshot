import React, { useState } from "react";
import { useStripe, useElements, CardElement } from "@stripe/react-stripe-js";
import {
  SideSheet,
  Heading,
  Pane,
  TextInput,
  Label,
  Button,
  Paragraph,
  Text,
} from "evergreen-ui";
import { createPayment } from "services/payments";

const PurchaseSheet = (props) => {
  const { product, isShown, onCloseComplete } = props;
  const [state, setState] = useState({ step: "capture" });
  const stripe = useStripe();
  const elements = useElements();

  const cardElementOptions = {
    style: {
      base: {
        color: "#425A70",
        fontFamily:
          "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
        fontSize: "16px",
        "::placeholder": {
          color: "#E4E7EB",
        },
      },
      invalid: {
        color: "#EC4C47",
        iconColor: "#EC4C47",
      },
    },
  };

  const handleContinueToCardCapture = async (event) => {
    // Handles continuing to step 2 [card] (after filling the email address)
    event.preventDefault();
    setState({ ...state, isLoading: true });
    const response = await createPayment({
      email: state.email,
      product_id: product.id,
    });

    if (response.status !== 201) {
      setState({ ...state, isLoading: false });
      return;
    }

    setState({
      ...state,
      isLoading: false,
      step: "card",
      stripeClientSecret: response.data.client_secret,
    });
  };

  const handlePurchase = async (event) => {
    event.preventDefault();
    const result = await stripe.confirmCardPayment(state.stripeClientSecret, {
      payment_method: {
        card: elements.getElement(CardElement),
      },
    });

    if (result.error) {
      // Show error to your customer (e.g., insufficient funds)
      console.log(result.error.message);
    } else {
      // The payment has been processed!
      if (result.paymentIntent.status === "succeeded") {
        // Show a success message to your customer
        // There's a risk of the customer closing the window before callback
        // execution. Set up a webhook or plugin to listen for the
        // payment_intent.succeeded event that handles any business critical
        // post-payment actions.
      }
    }
  };

  const handleCardInputChange = (changeObject) => {
    if (changeObject.error) {
      setState({
        ...state,
        purchaseReady: false,
        cardInputError: changeObject.error.message,
      });
    } else {
      setState({ ...state, cardInputError: null });
    }

    if (changeObject.complete) {
      setState({ ...state, purchaseReady: true });
    }
  };

  return (
    <>
      {product && (
        <SideSheet isShown={isShown} onCloseComplete={onCloseComplete}>
          <img src={`images/${product.id}.jpg`} alt="" />
          <Pane display="flex" flexDirection="column" padding={32}>
            <Heading size={600} marginTop={0}>
              {product.name} ready for purchase 🛍
            </Heading>
            <Paragraph marginBottom={28}>{product.description}</Paragraph>
            {state.step === "capture" && (
              <>
                <Label>Your email address</Label>
                <form onSubmit={handleContinueToCardCapture}>
                  <TextInput
                    onChange={(e) =>
                      setState({ ...state, email: e.target.value })
                    }
                    value={state.email}
                    placeholder="luke@themoon.org"
                    autoFocus={isShown}
                    required
                  />
                  <div style={{ marginTop: 32 }}>
                    <Button type="submit" isLoading={state.isLoading}>
                      Next
                    </Button>
                  </div>
                </form>
              </>
            )}
            {state.step === "card" && (
              <>
                <form onSubmit={handlePurchase}>
                  <Label>Please enter your card information below.</Label>
                  <CardElement
                    onReady={(el) => el.focus()}
                    onChange={handleCardInputChange}
                    options={cardElementOptions}
                  />
                  {state.cardInputError && (
                    <Text color="#EC4C47" marginTop={16}>
                      {state.cardInputError}
                    </Text>
                  )}
                  <div style={{ marginTop: 32 }}>
                    <Button
                      type="submit"
                      isLoading={state.isLoading}
                      disabled={!stripe || !elements || !state.purchaseReady}
                      appearance="primary"
                    >
                      Purchase now
                    </Button>
                  </div>
                </form>
              </>
            )}
          </Pane>
        </SideSheet>
      )}
    </>
  );
};

export default PurchaseSheet;
