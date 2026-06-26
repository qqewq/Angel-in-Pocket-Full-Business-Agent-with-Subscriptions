from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..auth import get_current_user
from ..config import settings
from ..services.payment.stripe_gateway import StripeGateway
import stripe
import json

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])
stripe.api_key = settings.stripe_secret_key

PLANS = {
    "pro": {
        "name": "Pro",
        "price_id": "price_1XXXXX",  # replace with your Stripe Price ID
        "amount": 2900,  # $29.00
        "currency": "usd",
        "description": "Unlimited projects, GRA nullification, accounting & tax"
    },
    "enterprise": {
        "name": "Enterprise",
        "price_id": "price_2XXXXX",
        "amount": 9900,
        "currency": "usd",
        "description": "Everything in Pro plus custom integrations and priority support"
    }
}

@router.get("/plans")
def list_plans():
    return PLANS

@router.post("/create-checkout-session")
async def create_checkout_session(
    plan: str = "pro",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if plan not in PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan")
    price_id = PLANS[plan]["price_id"]
    gateway = StripeGateway()
    # Ensure customer exists
    customer_id = current_user.stripe_customer_id
    if not customer_id:
        customer = stripe.Customer.create(email=current_user.email)
        customer_id = customer.id
        current_user.stripe_customer_id = customer_id
        db.commit()
    checkout_session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url="http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:3000/cancel",
    )
    return {"url": checkout_session.url}

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400)

    # Handle the event
    from ..database import SessionLocal
    db = SessionLocal()
    try:
        if event["type"] == "customer.subscription.updated":
            subscription = event["data"]["object"]
            customer_id = subscription["customer"]
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if user:
                status = subscription["status"]
                if status == "active":
                    # Map product to tier – in a real app, fetch price and map to plan
                    items = subscription["items"]["data"]
                    # Simplified: if any item is pro price -> pro, else enterprise
                    pro_price = PLANS["pro"]["price_id"]
                    ent_price = PLANS["enterprise"]["price_id"]
                    tier = "pro" if any(i["price"]["id"] == pro_price for i in items) else "enterprise"
                    user.subscription_tier = tier
                    import datetime
                    user.subscription_end_date = datetime.datetime.fromtimestamp(subscription["current_period_end"])
                elif status == "past_due":
                    # Optionally downgrade
                    pass
                elif status in ["canceled", "unpaid"]:
                    user.subscription_tier = "free"
                    user.subscription_end_date = None
                db.commit()
        elif event["type"] == "customer.subscription.deleted":
            subscription = event["data"]["object"]
            customer_id = subscription["customer"]
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if user:
                user.subscription_tier = "free"
                user.subscription_end_date = None
                db.commit()
    finally:
        db.close()
    return {"status": "success"}

@router.post("/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No active subscription")
    subscriptions = stripe.Subscription.list(customer=current_user.stripe_customer_id, status="active")
    for sub in subscriptions:
        stripe.Subscription.delete(sub.id)
    current_user.subscription_tier = "free"
    current_user.subscription_end_date = None
    db.commit()
    return {"status": "canceled"}
