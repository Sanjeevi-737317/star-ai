import json
import logging
import os

import httpx
from groq import AsyncGroq

from app.schemas.quotation import QuotationExtractedData

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")


class STARAI:
    def __init__(self):
        self.client = AsyncGroq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

    async def analyze_quotation(self, text: str, rfq_context: dict | None = None) -> QuotationExtractedData:
        if not self.client:
            raise RuntimeError("GROQ_API_KEY not configured")

        prompt = (
            "Extract structured quotation data from the provided text and return ONLY valid JSON matching this schema:\n"
            "{\n"
            '  "vendor_name": "string",\n'
            '  "quotation_number": "string",\n'
            '  "currency": "string",\n'
            '  "items": [{"name": "string", "quantity": 0, "unit_price": 0.0, "discount": 0.0}],\n'
            '  "subtotal": 0.0,\n'
            '  "tax": 0.0,\n'
            '  "shipping": 0.0,\n'
            '  "total": 0.0,\n'
            '  "delivery_days": 0,\n'
            '  "payment_terms": "string",\n'
            '  "warranty": "string",\n'
            '  "risks": ["string"]\n'
            "}\n\n"
            f"RFQ Context: {json.dumps(rfq_context or {})}\n\nQuotation text:\n{text}"
        )

        try:
            completion = await self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="groq/compound",
                temperature=0.1,
                response_format={"type": "json_object"},
            )
            content = completion.choices[0].message.content
            data = json.loads(content)
            return QuotationExtractedData(**data)
        except Exception as exc:
            logger.exception("Groq analysis failed")
            raise

    async def get_recommendation(self, rfq_id: int, scores: list[dict], tco_data: dict, risk_data: dict) -> str:
        prompt = (
            f"Provide a concise procurement recommendation for RFQ {rfq_id}.\n"
            f"Scores: {json.dumps(scores)}\n"
            f"TCO: {json.dumps(tco_data)}\n"
            f"Risk: {json.dumps(risk_data)}\n"
            "Return a short recommendation string."
        )
        if not self.client:
            return "No AI recommendation available."

        try:
            completion = await self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="groq/compound",
                temperature=0.3,
            )
            return completion.choices[0].message.content.strip()
        except Exception:
            logger.exception("Recommendation generation failed")
            return "Recommendation unavailable due to AI service error."
