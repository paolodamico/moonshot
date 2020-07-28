import React from "react";
import { Pane, Text, Card, Heading, Button, Alert, Link } from "evergreen-ui";

const ProductCard = (props) => {
  const { product } = props;
  return (
    <Card
      elevation={1}
      width={300}
      marginLeft={16}
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
    >
      <img
        src={`images/${product.id}.jpg`}
        alt=""
        width="100%"
        style={{ borderRadius: "5px 5px 0 0" }}
      />
      <Pane
        border="none"
        display="flex"
        alignItems="center"
        justifyContent="center"
        marginBottom={32}
        width="100%"
      >
        <div style={{ flexGrow: 1, paddingLeft: 16, paddingRight: 16 }}>
          <Heading size={600} marginTop="default">
            {product.name} - ${product.price / 100} {product.currency}
          </Heading>
          <Text>{product.description}</Text>
        </div>
        <div style={{ paddingRight: 16, marginTop: 28 }}>
          <Button alignSelf="flex-end" appearance="primary">
            Purchase
          </Button>
        </div>
      </Pane>
    </Card>
  );
};

const Home = () => {
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

  return (
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
          <ProductCard product={product} key={product.id} />
        ))}
      </Pane>
    </Pane>
  );
};

export default Home;
