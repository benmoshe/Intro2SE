# This works. Your job is to make it readable without breaking it.
# See README.md for the helpers the tests expect you to extract.


def order_total(o):
    t = 0
    for i in o["items"]:
        t = t + i["price"] * i["quantity"]
    # discount
    if o["tier"] == "gold":
        t2 = t - t * 0.2
    else:
        if o["tier"] == "silver":
            t2 = t - t * 0.1
        else:
            t2 = t
    # shipping
    if t2 > 100:
        s = 0
    else:
        s = 5.99
    x = t2 * 0.08
    r = t2 + x + s
    return round(r, 2)
