import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(instance):
    """Создаем продукт в stripe."""

    title_product = (
        f"{instance.paid_course}" if instance.paid_course else f"{instance.paid_lesson}"
    )
    stripe_product = stripe.Product.create(name=f"{title_product}")
    return stripe_product.get("id")


def create_stripe_price(product_id, amount):
    """Создает цену в stripe."""

    return stripe.Price.create(
        currency="usd",
        unit_amount=int(amount * 100),
        product=product_id
    )


def create_stripe_session(price):
    """Создает сессию на оплату в stripe."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
