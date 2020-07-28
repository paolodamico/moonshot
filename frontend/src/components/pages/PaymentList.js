import React, { useEffect, useState } from "react";
import { fetchPayments } from "services/payments";
import {
  Table,
  Pane,
  Heading,
  BackButton,
  Avatar,
  Badge,
  Alert,
  Text,
} from "evergreen-ui";
import { Link } from "react-router-dom";

const PaymentList = () => {
  const [state, setState] = useState({});

  const statusMapping = {
    created: "neutral",
    paid: "green",
    requires_action: "yellow",
    cancelled: "red",
    fulfilled: "purple",
  };

  useEffect(() => {
    async function fetchData() {
      const response = await fetchPayments();
      setState((s) => ({ ...s, data: response.data.results }));
    }
    fetchData();
  }, []);

  return (
    <>
      <Heading
        size={800}
        marginTop="default"
        marginLeft={64}
        marginBottom={28}
        style={{ display: "flex", alignItems: "center" }}
      >
        <Link to="/" style={{ textDecoration: "none", marginRight: 16 }}>
          <BackButton />
        </Link>
        Payments history list
      </Heading>
      <Alert
        intent="none"
        title="Not all data is shown!"
        marginTop={32}
        marginBottom={32}
        width="100%"
        marginRight={64}
        marginLeft={64}
      >
        <Text>
          As this is a test project, only the last 100 payments are shown. To
          view older payments please use the Django console or connect directly
          to the database.
        </Text>
      </Alert>
      <Pane marginRight={64} marginLeft={64}>
        {state.data && (
          <Table>
            <Table.Head>
              <Table.TextHeaderCell
                flexBasis={54}
                flexShrink={0}
                flexGrow={0}
              ></Table.TextHeaderCell>
              <Table.TextHeaderCell>Email</Table.TextHeaderCell>
              <Table.TextHeaderCell>Product ID</Table.TextHeaderCell>
              <Table.TextHeaderCell>Amount</Table.TextHeaderCell>
              <Table.TextHeaderCell>Currency</Table.TextHeaderCell>
              <Table.TextHeaderCell>Status</Table.TextHeaderCell>
              <Table.TextHeaderCell>UUID</Table.TextHeaderCell>
            </Table.Head>
            <Table.Body height="100%">
              {state.data.map((payment) => (
                <Table.Row key={payment.uuid}>
                  <Table.TextCell flexBasis={54} flexShrink={0} flexGrow={0}>
                    <Avatar name={payment.email} size={28} />
                  </Table.TextCell>
                  <Table.TextCell>{payment.email}</Table.TextCell>
                  <Table.TextCell>{payment.product_id}</Table.TextCell>
                  <Table.TextCell isNumber>
                    ${payment.amount / 100}
                  </Table.TextCell>
                  <Table.TextCell>{payment.currency}</Table.TextCell>
                  <Table.TextCell>
                    <Badge color={statusMapping[payment.status]}>
                      {payment.status}
                    </Badge>
                  </Table.TextCell>
                  <Table.TextCell>{payment.uuid}</Table.TextCell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table>
        )}
      </Pane>
    </>
  );
};

export default PaymentList;
