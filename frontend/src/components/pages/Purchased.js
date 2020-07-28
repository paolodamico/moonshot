import React from "react";
import {
  Card,
  Heading,
  Pane,
  TickCircleIcon,
  Text,
  Button,
} from "evergreen-ui";
import { Link, useLocation } from "react-router-dom";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const Purchased = () => {
  const query = useQuery();
  const name = query.get("name");

  return (
    <>
      <Pane display="flex" justifyContent="center">
        <Card
          padding={32}
          elevation={1}
          marginTop={64}
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          maxWidth={400}
        >
          <TickCircleIcon color="success" marginRight={16} size={100} />
          <Heading
            size={800}
            marginTop={16}
            color="#47B881"
            textAlign="center"
            marginBottom={64}
          >
            Your {name} purchase has been completed!
          </Heading>

          <Text textAlign="center" style={{ marginBottom: 32 }}>
            You may now close this window. You will receive a receipt in your
            email shortly.
          </Text>
          <Link to="/" style={{ textDecoration: "none" }}>
            <Button>Continue browsing</Button>
          </Link>
        </Card>
      </Pane>
    </>
  );
};

export default Purchased;
