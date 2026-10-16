TAX_RATE = 0.08
STANDARD_SHIPPING = 5.99
FREE_SHIPPING_THRESHOLD = 100
DISCOUNT_RATES = {"gold": 0.2, "silver": 0.1}


def subtotal(items):
    return sum(item["price"] * item["quantity"] for item in items)


def discount_rate(tier):
    return DISCOUNT_RATES.get(tier, 0.0)


def shipping_cost(amount):
    if amount > FREE_SHIPPING_THRESHOLD:
        return 0.0
    return STANDARD_SHIPPING


def order_total(order):
    gross = subtotal(order["items"])
    discounted = gross * (1 - discount_rate(order["tier"]))
    tax = discounted * TAX_RATE
    return round(discounted + tax + shipping_cost(discounted), 2)
