This document contains logged interactions with the Stripe's ecosystem (API, documentation, libraries, etc.). The goal is providing feedback for potential improvements to the [Stripe PaymentIntents](https://stripe.com/docs/api/payment_intents) integration experience. To faciliate the above, the document is annotated with the follwing emojis:

- 🔥 Friction
- 💕 Great experience
- 🚀 Potential improvement

> 💡 The implementation of this project was based on [this guide][guide]. Useful to keep in mind while going through this document.

## General

Feedback pertaining to general matters related to payments is contained in this section.

- 🚀 For a **new Stripe user** a way to understand the trade-offs between using [Checkout](https://stripe.com/payments/checkout) and [Elements](https://stripe.com/payments/elements) might be useful. While doing a fully customized API implementation (e.g. PCI level 1 merchants) might be an edge case for advanced users, deciding between Checkout and Elements seems like a decision for most mainstream merchants.
- 💕 The [guide][guide] contained quick instructions and relevant code snippets to get everything up and running quickly. Most things were addressed there and made the experience very simple.
- 💕 The [automatic tests](https://stripe.com/docs/payments/accept-a-payment#web-test-integration) was a great way to make sure the integration was fully working as expected. It also provides the developer with a measurable sense of accomplishment.

## Backend

Feedback pertaining to the backend (server-to-serve, API) integration is contained in this section.

- 🔥 From the [guide][guide], it was not clear what are the transition between the different statuses that a `PaymentIntent` may take, and further which of those statuses are relevant for a simple E2E integration. While the statuses as explained [here](https://stripe.com/docs/payments/intents#intent-statuses) makes it more clear, details on what statuses to listen for on the customer's end was not 100% clear.

  - Additionally, the `requires_payment_method` transition after a failed payment is not intutive (vs. other models in which there is a terminal `declined` state) and while it makes a lot of sense (to allow retries on the same `PaymentIntent`), better clarification (communication) could be helpful.

- 💕 Installing [stripe-python](https://github.com/stripe/stripe-python) and getting it working was super simple and straightforward. Additionally, contrary to a myriad of other providers in the payments space, only the few really necessary attributes are actually required to make a request to create a `PaymentIntent`.

- 🚀 The [Prices API](https://stripe.com/docs/api/prices) can be very useful even for simple integrations as it can leverage Stripe's infrastructure to store and manage the products and price listings (e.g. removes the necessity of validating prices on the merchant's API or can make us of Stripe's dashboard to manage them). There was no mention of this in the [guide][guide] and an example where even the product listing comes from Stripe could prove very powerful.

- 🔥 The [guide][guide] was not explicitly clear on how to handle payment authentication (e.g. 3DS), whether Stripe.js handles it automatically and whether any action on the backend was required. After testing out the entire flow, the experience as amazing 💕 because 3DS and other authentication methods are supported out of the box, however this was not understood from the beginning.

- 🔥 Handling Stripe's webhooks (particularly in testing mode) presented a small issue, because Stripe actually sends a beautified JSON string on the webhook's payload which was something Django's [HTTP Client](https://docs.djangoproject.com/en/3.0/ref/request-response/) and [DRF](https://www.django-rest-framework.org/api-guide/testing/) did not correctly handle by default. DRF recognizes the `Content-Type` header and attempts to parse the body directly, and this raised parsing exceptions. A custom parser had to be implemented (see `backend/api/parsers.py` for details). For testing, this also implied simulating the beautified text-based body (see `backend/api/tests/test_webhooks.py` for an example). Might be a DRF-only issue.

- 🚀 The `stripe.Webhook.construct_event` that parses the webhook raw body and validates the signature worked successfully even if the webhook is malformed (e.g. if the webhook contains no `data` or an invalid object in `data`). To be clear invalid JSON is not accepted, however further validating the schema of the webhook might be helpful to remove the overhead on the developer's side to handle edge cases of malformed requests.

## Frontend

Feedback pertaining to the frontend (client libraries, UI/UX) integration is contained in this section.

- 🔥 The [guide][guide] instructs the developer to set the `Elements` provider on the root of the application. However this might not be ideal for all cases, adding this extra provider can increase the overhead on the overall website when the payment flow may be accessed only by some users.
  - 🚀 Perhaps there are benefits of having the `Elements` provider in the root (e.g. I imagine that Stripe collects some signals to run Radar's fraud analysis), maybe these benefits can be better communicated so the developer can make an informed decision.
  - 🚀 If a developer does decide to only implement the `Elements` provider on the payments-scoped component (and not on the root component), there is no guide on how to correctly use in the same component with the functional hoooks (e.g. `useElements`). Perhaps the hooks are not needed if used directly in a component.
- 🚀 The sample code snippet on [this step](https://stripe.com/docs/payments/accept-a-payment#web-submit-payment) validates `!stripe || !elements` on line 15, but only `!stripe` on line 48, this caused some confusion on whether the `!elements` was actually needed or not. Perhaps the double validation might not be required?

- 🚀 There is a great example on how to autofocus the `CardElement` initial input (see snippet below). This seems like a very common occurrence, perhaps a specific property (e.g. `focusOnReady`) that wraps this code might be even better?

  ```jsx
  <CardElement onReady={(el) => el.focus()} />
  ```

- 🔥 There was some friction in understanding how validating the `CardElement` input(s) work (e.g. expired card number, actual details found [here](https://github.com/stripe/react-stripe-elements#props-shape-2)). This was not found on the [guide][guide] even though the guide instructs you to handle error cases (and is a fairly critical UX element).
  - 🚀 Most integrations would only show an error message below or above the `CardElement` component with the error details. As this seems like a fairly common case why not add a prop (e.g. `showInputErrors`) to `CardElement` that allows showing such error messages automatically. Further, having this option as a default would ensure a more consistent/useful UX for end-users and likely increase conversion for merchants.

* 🔥 There was some friction understanding how the zip code input (on by default on `CardElement`) works. At first, I imagined only US zip codes (because of the accepted format) were supported and that I would have to enable some additional prop or implement my custom integration. After browsing the documentation for a while I found [this reference](https://stripe.com/docs/js/element/postal_code_formatting) that explains how the zip code validation is set based on the card's issuing country (likely by BIN). Perhaps adding a note in the guide explaining that Elements is fully ready to support any country's card and zip code might reduce friction here.

* 💕 The overall installation and usage experience was great, just a few lines of code to get everything up and running. The React library is very robust and customisation was straightforward.

[guide]: https://stripe.com/docs/payments/accept-a-payment
