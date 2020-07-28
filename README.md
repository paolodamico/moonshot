# Moonshot

Moonshot is a sample project to test Stripe's [PaymentIntents](https://stripe.com/docs/api/payment_intents) API.

<img src="feedback-log/images/moonshot-home.jpg?raw=true" width="600" />

## 👨‍💻Running locally

This repository contains separate frontend and backend (REST API) components. The frontend is built on [React.js](https://github.com/facebook/react/) and the backend is built on [Django REST framework](https://github.com/encode/django-rest-framework). Both environments are required to properly run this application. This section will guide you on setting up both environments.

1. Install Python 3.8 ([pyenv](https://github.com/pyenv/pyenv) recommended) and [Node.js](https://nodejs.org/en/download/).
1. Clone the repository and `cd` into the project directory.
1. Set-up and activate a virtual environment (for Python).
   ```bash
   python3 -m venv env && source env/bin/activate
   ```
1. Install the projects dependencies
   ```bash
   make install
   ```
1. Install [Stripe CLI](https://stripe.com/docs/payments/handling-payment-events#install-cli), login and listen for webhooks.
   ```bash
   brew install stripe/stripe-cli/stripe # adjust command to your OS / preferences
   stripe login
   stripe listen --forward-to http://localhost:8000/webhook/
   ```
1. Set the following environment variables (a [Stripe Secret Key](https://stripe.com/docs/keys) will be required). **Do not use the sample values provided below**.

   ```bash
    export STRIPE_API_KEY=sk_test_L5UPP43S7sZCE29pd6O
    export STRIPE_WEBHOOK_SECRET=whsec_oOgN7Ec0JPKVTjuTflKvO7 # obtained from Stripe CLI (previous step; last command)
   ```

1. Set the corresponding **publishable key** on `frontend/src/constants.js` file (line 2). **Do not use the sample value provided below**.
   ```js
   export const STRIPE_PUBLIC_KEY = "pk_test_RBFqFUXP02gVq00UX2gVbi";
   ```
1. Run the tests to make sure everything works as expected
   ```bash
   make test
   ```
1. Run the API & frontend
   ```bash
   make start
   ```
1. Browse the local version on [`http://localhost:3000/`](http://localhost:3000/) (FYI API will run on `http://localhost:8000`)

## 🧪 Testing

The backend REST API follows a [Test-driven development](https://en.wikipedia.org/wiki/Test-driven_development) approach, making use of functional testing to ensure no breaking changes are introduced on code updates. To run the tests, the following command can be used (**N.B. be sure to activate the virtual environment before running the tests**),

```bash
make test
```

A few details on the testing implementation:

- This product relies on Stripe's API to process mission-critical flows. To ensure consistency, offline availability and speedy processing times, in testing mode, [VCR.py](https://github.com/kevin1024/vcrpy) is used to mock Stripe's response. Therefore, the API will **not be hit during tests**.

## 📑Feedback log

As part of this project, a detailed [feedback log](/feedback-log/README.md) was kept to record any friction points, potential improvements, and useful/helpful interactions. The log can be viewed [here](/feedback-log/README.md).

## 🚀Features

This project follows [this guide](https://stripe.com/docs/payments/accept-a-payment) and as such incorporates the following features:
- An internal list of products and prices with a user interface to see the products and descriptions on the home page.
- The user can select any of the products to purchase.
   - They will be asked for their email address, and the API will create a `PaymentIntent` on Stripe.
   - They will then be asked to enter their payment information using Stripe [Elements](https://stripe.com/payments/elements).
   - If the payment fails an error message will be shown at the top of the screen and the user will be able to retry the payment (see [Stripe Testing](https://stripe.com/docs/testing) for sample card numbers that simulate failures).
   - If the payment is successful the user is taken to a payment confirmation screen.
- The API will listen for Stripe's `payment_intent.succeeded` webhook to internally mark the `PaymentIntent` as `paid`. The webhook will validate that the webhook comes from Stripe using the [signature validation](https://stripe.com/docs/webhooks/signatures) mechanism. _To use locally [Stripe CLI](https://stripe.com/docs/stripe-cli) will be required._
- The project also incorporates a user interface to list all payments on http://localhost:3000/list. This can be used to verify that the webhook was properly received and handled.
- The project will easily run through the [automated testing](https://stripe.com/docs/payments/accept-a-payment#web-test-integration) by executing the payments with the provided card numbers. Below is the expected results after doing all three payments.

<img src="feedback-log/images/moonshot-tests.jpg?raw=true" width="600" />

> :warning: This is a test project not intended for production. Security issues (such as secret keys, debugging mode), performance issues or production-ready elements (e.g. not using SQLite as the database engine) are not covered as they are out of the scope of this project. **Do not use in production.**

## 💛Attributions
A special thanks to the following people/entities (plus any other project dependencies):
- [Pexels](https://www.pexels.com/) for stock photos.
- [Unsplash](https://unsplash.com/) for stock photos.
- [Evergreen](https://evergreen.segment.com) for the UI components.

## 👩‍⚖️License
This project is licensed under an [MIT license](/LICENSE). Free to use, distribute and modify for personal and commercial use. License and copyright notice should be posted.