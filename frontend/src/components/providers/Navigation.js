import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import { Home, Purchased, PaymentList } from "components/pages";

const NavigationProvider = () => (
  <BrowserRouter>
    <Switch>
      <Route path="/purchased" exact>
        <Purchased />
      </Route>
      <Route path="/list" exact>
        <PaymentList />
      </Route>
      <Route path="/">
        <Home />
      </Route>
    </Switch>
  </BrowserRouter>
);

export default NavigationProvider;
