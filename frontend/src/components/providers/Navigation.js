import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import { Home, Purchased } from "components/pages";

const NavigationProvider = () => (
  <BrowserRouter>
    <Switch>
      <Route path="/purchased">
        <Purchased />
      </Route>
      <Route path="/">
        <Home />
      </Route>
    </Switch>
  </BrowserRouter>
);

export default NavigationProvider;
