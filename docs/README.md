# Angel in Pocket – Full Business Agent with Subscriptions

A full-stack business agent powered by the GRA (Generative Resonance Architecture) stability core, with paid subscription tiers via Stripe.

## Architecture

- **gra_core/** – GRA stability engine, multiverse adapter, and client
- **angel/** – Business logic agents (idea intake, product design, finance, accounting, tax, etc.)
- **app/** – FastAPI backend with JWT auth, Stripe subscriptions, and REST API
- **frontend/** – React + TypeScript frontend

## Subscription Tiers

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 1 project, basic idea intake |
| Pro | $29/mo | Unlimited projects, GRA nullification, accounting & tax |
| Enterprise | $99/mo | Everything + custom integrations, priority support |

## Setup

1. Install Python deps: `pip install -r requirements.txt`
2. Set up `.env` from `.env.example`
3. Configure Stripe products/prices and update `price_id` placeholders
4. Run: `uvicorn app.main:app --reload`
5. Forward Stripe webhooks: `stripe listen --forward-to localhost:8000/subscriptions/webhook`
6. Start frontend: `cd frontend && npm start`

## API Overview

- `POST /auth/register` – Create account
- `POST /auth/login` – Get JWT token
- `POST /ideas/` – Submit business idea
- `POST /projects/{id}/launch` – Launch project (Pro required)
- `POST /subscriptions/create-checkout-session` – Upgrade plan
- `POST /subscriptions/webhook` – Stripe webhook handler
