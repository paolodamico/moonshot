import React, { useState } from "react";
import { Pane, Text, Heading, Alert, Link } from "evergreen-ui";
import { ProductCard, PurchaseSheet } from "components/common";

const Home = () => {
  const [state, setState] = useState({
    purchaseSheetShown: false,
    product: null,
  });
  const products = [
    {
      id: "photoshoot",
      name: "Photoshoot",
      description:
        "Your very own photoshoot in the moon (includes non-atomsphere-friendly green screen).",
      price: 19999,
      currency: "USD",
    },
    {
      id: "troubleshoot",
      name: "Troubleshoot",
      description:
        "Problems with your spaceship, biodome, or space fridge? Will diagnose and fix everything.",
      price: 399999,
      currency: "GBP",
    },
    {
      id: "peashoot",
      name: "Pea shoot",
      description:
        "Try our amazing cryopreserved pea shoots. Tastes just like on Earth. Ships in 1-3 full moons.",
      price: 1499,
      currency: "USD",
    },
  ];

  const handlePurchase = (product) => {
    setState({ purchaseSheetShown: true, product });
  };

  return (
    <>
      <Pane
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="flex-start"
        border="default"
      >
        <Heading size={800} marginTop="default">
          Welcome to Moonshot!
        </Heading>

        <Text>
          You one-stop shop for{" "}
          <span role="img" aria-label="">
            🌑
          </span>{" "}
          Moon products.
        </Text>

        <Alert
          intent="none"
          title="This is not a real company!"
          marginTop={32}
          width="100%"
          maxWidth={1000}
        >
          <Text>
            This is a sample project to test a{" "}
            <Link
              target="_blank"
              rel="noopener noreferrer"
              href="https://stripe.com/docs/payments/accept-a-payment"
            >
              payments integration
            </Link>{" "}
            with{" "}
            <Link
              target="_blank"
              rel="noopener noreferrer"
              href="https://stripe.com"
            >
              Stripe
            </Link>
            .
          </Text>
        </Alert>

        <Pane
          display="flex"
          alignItems="center"
          justifyContent="center"
          border="default"
          margin={64}
          marginTop={32}
          maxWidth={1000}
          padding={32}
          paddingLeft={16}
          width="100%"
        >
          {products.map((product) => (
            <ProductCard
              product={product}
              key={product.id}
              handlePurchase={() => handlePurchase(product)}
            />
          ))}
        </Pane>
      </Pane>
      <PurchaseSheet
        isShown={state.purchaseSheetShown}
        onCloseComplete={() =>
          setState({ ...state, purchaseSheetShown: false })
        }
        product={state.product}
      />
    </>
  );
};

export default Home;
