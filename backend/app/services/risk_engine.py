import logging
import statistics

logger = logging.getLogger(__name__)


def analyze_risk(quotation: dict, vendor: dict, rfq: dict) -> dict:
    risks = []
    total = float(quotation.get("total") or 0)

    totals = [float(q.get("total") or 0) for q in quotation.get("all_quotations", [])]
    avg = statistics.mean(totals) if totals else total or 1.0

    if total > 0 and total < 0.5 * avg:
        risks.append("Unusually low price compared to average")
    if (quotation.get("payment_terms") or "").lower().count("advance") and "100%" in (quotation.get("payment_terms") or ""):
        risks.append("100% advance payment required")
    if (quotation.get("delivery_days") or 0) > 30:
        risks.append("Long delivery period")
    if not quotation.get("warranty"):
        risks.append("No warranty specified")
    if float(quotation.get("shipping") or 0) > 0.1 * (total or 1):
        risks.append("Extra freight charges")
    if quotation.get("cancellation_penalty"):
        risks.append("Cancellation penalty present")
    if not quotation.get("items"):
        risks.append("Missing item details")
    if quotation.get("expired"):
        risks.append("Quotation expired")

    risk_score = min(100.0, len(risks) * 15.0)
    if risk_score >= 60:
        level = "HIGH"
    elif risk_score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": round(risk_score, 2),
        "risk_level": level,
        "risks": risks,
        "vendor_id": vendor.get("id"),
        "rfq_id": rfq.get("id"),
    }
