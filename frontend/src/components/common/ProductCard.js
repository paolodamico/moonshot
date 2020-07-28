import React from "react";
import { Pane, Text, Card, Heading, Button } from "evergreen-ui";

const ProductCard = (props) => {
  const { product, handlePurchase } = props;
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
          <Button
            alignSelf="flex-end"
            appearance="primary"
            onClick={handlePurchase}
          >
            Purchase
          </Button>
        </div>
      </Pane>
    </Card>
  );
};

export default ProductCard;
