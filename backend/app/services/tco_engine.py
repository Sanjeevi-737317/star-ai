import logging

logger = logging.getLogger(__name__)


def calculate_tco(quotation: dict, vendor: dict) -> dict:
    base_price = float(quotation.get("subtotal") or 0.0)
    shipping = float(quotation.get("shipping") or 0.0)
    tax = float(quotation.get("tax") or 0.0)
    discounts = sum(float(item.get("discount") or 0.0) for item in quotation.get("items", []))

    installation = 0.0
    handling = 0.0
    other_charges = 0.0

    tco = base_price + shipping + installation + handling + other_charges - discounts + tax
    explanation = (
        f"Base price: {base_price:.2f}, Shipping: {shipping:.2f}, "
        f"Tax: {tax:.2f}, Discounts: {discounts:.2f}. "
        f"Estimated TCO: {tco:.2f}"
    )
    return {
        "tco": round(tco, 2),
        "base_price": base_price,
        "shipping": shipping,
        "tax": tax,
        "discounts": discounts,
        "explanation": explanation,
    }
