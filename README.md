# Moonshot

Moonshot is a sample project to test Stripe's [PaymentIntents](https://stripe.com/docs/api/payment_intents) API.

<img src="feedback-log/images/moonshot-home.jpg?raw=true" width="600" />

## 👨‍💻Running locally

This repository contains separated frontend and backend (REST API) components. The frontend is built on [React.js](https://github.com/facebook/react/) and the backend is built on [Django REST framework](https://github.com/encode/django-rest-framework). Both environments are required to properly run this application. This section will guide you on setting up both environments.

1. Install Python 3.8 ([pyenv](https://github.com/pyenv/pyenv) recommended) and [Node.js](https://nodejs.org/en/download/).
1. Clone the repository and `cd` into the project directory.
1. Set-up and activate a virtual environment.
   ```bash
   python3 -m venv env && source env/bin/activate
   ```
1. Install the projects dependencies
   ```bash
   make install-test
   ```
1. Install [Stripe CLI](https://stripe.com/docs/payments/handling-payment-events#install-cli), login and listen for webhooks.
   ```bash
   brew install stripe/stripe-cli/stripe # adjust to your OS / preferences
   stripe login
   stripe listen --forward-to http://localhost:8000/webhook/
   ```
1. Set the following environment variables (a [Stripe Secret Key](https://stripe.com/docs/keys) will be required).

   ```bash
    export STRIPE_API_KEY=sk_test_L5UPP43S7sZCE29pd6O
    export STRIPE_WEBHOOK_SECRET=whsec_oOgN7Ec0JPKVTjuTflKvO7 # obtained from Stripe CLI (previous step; last command)
   ```

1. Set the corresponding **publishable key** on `frontend/src/constants.js` file: 2
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
