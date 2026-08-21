import logging

logger = logging.getLogger(__name__)


WEIGHTS = {
    "price": 0.40,
    "delivery": 0.25,
    "reliability": 0.20,
    "terms": 0.15,
}


def normalize(score: float, max_value: float) -> float:
    if max_value <= 0:
        return 0.0
    return min(100.0, max(0.0, (score / max_value) * 100.0))


def calculate_scores(quotations: list[dict], rfq: dict) -> list[dict]:
    max_total = max(float(q.get("total") or 0) for q in quotations) or 1.0
    max_delivery = max(float(q.get("delivery_days") or 0) for q in quotations) or 1.0

    results = []
    for q in quotations:
        price_score = normalize(max_total - float(q.get("total") or 0), max_total)
        delivery_score = normalize(max_delivery - float(q.get("delivery_days") or 0), max_delivery)
        reliability_score = 70.0
        payment_score = 80.0

        final_score = (
            price_score * WEIGHTS["price"]
            + delivery_score * WEIGHTS["delivery"]
            + reliability_score * WEIGHTS["reliability"]
            + payment_score * WEIGHTS["terms"]
        )

        results.append({
            "quotation_id": q.get("id"),
            "vendor_id": q.get("vendor_id"),
            "rfq_id": rfq.get("id"),
            "price_score": round(price_score, 2),
            "delivery_score": round(delivery_score, 2),
            "reliability_score": round(reliability_score, 2),
            "payment_score": round(payment_score, 2),
            "final_score": round(final_score, 2),
        })
    return results
