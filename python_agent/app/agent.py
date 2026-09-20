from __future__ import annotations

import re
from typing import Any, Dict, Optional

from openai import OpenAI

from app.config import get_settings
from app.profile import Profile
from app.skills import SkillEngine


class CrossBorderAgent:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.profile = Profile()
        self.skills = SkillEngine(self.profile)
        self.client = OpenAI(api_key=self.settings.AISA_API_KEY, base_url=self.settings.AISA_BASE_URL) if self.settings.AISA_API_KEY else None

    def _parse_product_and_destination(self, message: str) -> tuple[str, str]:
        lower = message.lower()
        product = self.profile.facts.get("product") or "general product"
        destination = self.profile.facts.get("destination_market") or "South Korea"

        patterns = [
            r"for\s+(.+?)\s+in\s+([a-zA-Z ]+)",
            r"for\s+(.+?)\s+to\s+([a-zA-Z ]+)",
            r"selling\s+(.+?)\s+in\s+([a-zA-Z ]+)",
            r"sell\s+(.+?)\s+in\s+([a-zA-Z ]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, message, flags=re.IGNORECASE)
            if match:
                product = match.group(1).strip()
                destination = match.group(2).strip()
                break

        if "Japan" in message or "japan" in lower:
            destination = "Japan"
        elif "Germany" in message or "germany" in lower:
            destination = "Germany"
        elif "Brazil" in message or "brazil" in lower:
            destination = "Brazil"
        elif "South Korea" in message or "korea" in lower:
            destination = "South Korea"

        if "wireless earbuds" in lower or "earbuds" in lower:
            product = "wireless earbuds"
        elif "porcelain" in lower or "tableware" in lower:
            product = "porcelain tableware"
        elif "fitness" in lower or "home fitness" in lower:
            product = "home fitness products"

        return product, destination

    def generate_brief(
        self,
        destination: str,
        product: Optional[str] = None,
        market_language: str = "en",
        target_channel: str = "Amazon",
        price_band: str = "medium",
        constraints: Optional[list[str]] = None,
        budget: Optional[str] = None,
        notes: str = "",
    ) -> Dict[str, Any]:
        product_name = product or self.profile.facts.get("product") or "general consumer product"
        destination_name = destination or self.profile.facts.get("destination_market") or "South Korea"
        self.profile.add_fact("destination_market", destination_name)
        self.profile.add_fact("product", product_name)
        return self.skills.build_full_brief(
            destination_name,
            product_name,
            market_language=market_language,
            target_channel=target_channel,
            price_band=price_band,
            constraints=constraints,
            budget=budget,
            notes=notes,
        )

    def _model_call(self, prompt: str) -> str:
        if self.client is None:
            return (
                "AISA credentials are not configured. The project is running in local-safe mode. "
                "Set AISA_API_KEY in the .env file to enable live model calls."
            )

        response = self.client.chat.completions.create(
            model=self.settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a cross-border e-commerce market analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content or ""

    def handle_message(self, user_input: str) -> str:
        message = user_input.strip()
        if not message:
            return "Please provide a question or product idea."

        if self.profile.needs_interview():
            interview = self.skills.interview(message)
            self.profile.notes += f"Interview started: {message}\n"
            return (
                "\n".join(interview["questions"]) +
                "\n\n" + interview["message"]
            )

        lower = message.lower()
        product, destination = self._parse_product_and_destination(message)

        if "brief" in lower and ("full" in lower or "market" in lower or "report" in lower):
            return self._render_json(
                self.generate_brief(destination=destination, product=product)
            )

        if "trend" in lower or "trending" in lower or "demand" in lower:
            brief = self.skills.market_trends(destination, product)
            return self._render_json(brief)

        if "platform" in lower or "sell" in lower or "market" in lower:
            brief = self.skills.market_entry(destination, product)
            return self._render_json(brief)

        if "seo" in lower or "keyword" in lower:
            brief = self.skills.sku_seo(destination, product)
            return self._render_json(brief)

        self.profile.add_fact("destination_market", destination)
        self.profile.add_fact("product", product)
        brief = self.generate_brief(destination=destination, product=product)
        return self._render_json(brief)

    def _render_json(self, payload: Dict[str, Any]) -> str:
        from pprint import pformat

        return pformat(payload, width=120, sort_dicts=False)
