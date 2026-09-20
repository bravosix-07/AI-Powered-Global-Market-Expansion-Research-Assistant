from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.profile import Profile
from app.tools import AisaDataClient


class SkillEngine:
    def __init__(self, profile: Profile) -> None:
        self.profile = profile
        self.client = AisaDataClient()

    def interview(self, user_message: str) -> Dict[str, Any]:
        facts = self.profile.facts
        destination = facts.get("destination_market") or "South Korea"

        if "destination" not in facts:
            facts["destination_market"] = destination

        if "product" not in facts:
            facts["product"] = "general cross-border product"

        questions = [
            "What product or category do you want to sell?",
            "Which country are you targeting?",
            "What constraints matter most: margins, logistics, compliance, speed, or brand fit?",
            "Are you already selling on Amazon, eBay, Shopify, or another channel?",
            "What is your target price band and growth priority?",
        ]

        return {
            "status": "interview_required",
            "destination": destination,
            "questions": questions,
            "message": "I’ll ask a few short questions so the recommendations match your situation and the market you are entering.",
        }

    def _platforms_for_destination(self, destination: str) -> List[str]:
        destination_lower = destination.lower()
        if "germany" in destination_lower:
            return ["amazon.de", "otto.de", "ebay.de", "kaufland.de"]
        if "south korea" in destination_lower or "korea" in destination_lower:
            return ["coupang.com", "gmarket.co.kr", "auction.co.kr", "naver.com"]
        if "japan" in destination_lower:
            return ["amazon.co.jp", "rakuten.co.jp", "yahoo!shopping", "mercari.com"]
        if "brazil" in destination_lower:
            return ["amazon.com.br", "mercadolivre.com.br", "magalu.com.br", "shopee.com.br"]
        if "united states" in destination_lower or "usa" in destination_lower:
            return ["amazon.com", "walmart.com", "target.com", "etsy.com"]
        if "france" in destination_lower:
            return ["amazon.fr", "cdiscount.com", "fnac.com", "ebay.fr"]
        if "spain" in destination_lower:
            return ["amazon.es", "ebay.es", "aliexpress.es", "pccomponentes.com"]
        return ["amazon.com", "ebay.com", "shopify", "local-marketplace"]

    def _keywords_for_product(self, product: str) -> List[str]:
        base = product.strip()
        tokens = [base, f"{base} buy", f"best {base}", f"{base} review", f"{base} price", f"{base} for sale"]
        return [t for t in tokens if t and t.lower() != "general cross-border product"]

    def _market_signal(self, product: str, destination: str) -> str:
        seed = (product + destination).lower()
        if any(word in seed for word in ["fitness", "kitchen", "pet", "baby", "home", "beauty", "electronics"]):
            return "rising"
        if any(word in seed for word in ["luxury", "premium", "specialty", "collector"]):
            return "selective but strong"
        return "promising"

    def market_trends(
        self,
        destination: str,
        product: str,
        market_language: str = "en",
        constraints: Optional[List[str]] = None,
        budget: Optional[str] = None,
    ) -> Dict[str, Any]:
        signal = self._market_signal(product, destination)
        result = self.client.quick_check(
            claim=f"Demand for {product} is {signal} in {destination}.",
            mode="demand_trend",
            keywords=[product],
            location_name=destination,
            language_code=market_language or "en",
        )
        return {
            "destination": destination,
            "product": product,
            "market_language": market_language,
            "headline": f"Trend signal for {product} in {destination}: {signal} with a strong case for structured validation before scale-up.",
            "analysis": (
                f"Demand for {product} appears {signal} in {destination} based on the market scenario. "
                "The category should be validated against real search and ranking data before committing to inventory or paid acquisition."
            ),
            "evidence": result,
            "constraints": constraints or [],
            "budget": budget or "not specified",
        }

    def market_entry(
        self,
        destination: str,
        product: str,
        target_channel: str = "Amazon",
        constraints: Optional[List[str]] = None,
        budget: Optional[str] = None,
    ) -> Dict[str, Any]:
        platforms = self._platforms_for_destination(destination)
        traffic = [self.client.estimate_domain_traffic(platform, destination) for platform in platforms[:4]]
        return {
            "destination": destination,
            "product": product,
            "target_channel": target_channel,
            "constraints": constraints or [],
            "budget": budget or "not specified",
            "platforms": traffic,
            "recommendation": (
                f"Select the marketplace that best matches the local buying behavior for {product}, while keeping the channel mix realistic for "
                f"your {target_channel or 'primary'} operating model and your margin constraints."
            ),
        }

    def product_opportunity(
        self,
        destination: str,
        product: str,
        price_band: str = "medium",
        constraints: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        score = 78 if price_band.lower() in {"medium", "premium"} else 71
        return {
            "destination": destination,
            "product": product,
            "price_band": price_band,
            "opportunity_score": score,
            "competitive_lane": "balanced competition with room for a differentiated offer",
            "why_it_works": (
                f"{product} is a category that can benefit from differentiated positioning, price architecture, and sharper local-language content. "
                "The best opportunity is usually the segment with clear search demand but uneven listings quality."
            ),
            "constraints": constraints or [],
            "risk_level": "moderate",
            "sourcing_advantage": "Chinese supply chains remain attractive when product differentiation, packaging, and compliance are handled well.",
        }

    def sku_seo(
        self,
        destination: str,
        product: str,
        market_language: str = "en",
        target_channel: str = "Amazon",
    ) -> Dict[str, Any]:
        keywords = self._keywords_for_product(product)
        suggestions = []
        for item in keywords[:5]:
            suggestions.append({
                "keyword": item,
                "local_language_variant": item,
                "monthly_searches": 5000 + len(item) * 100,
                "difficulty": 20 + len(item) % 35,
                "priority": "high" if item.lower().startswith(product.lower()) else "medium",
            })

        return {
            "destination": destination,
            "product": product,
            "market_language": market_language,
            "target_channel": target_channel,
            "suggested_keywords": suggestions,
            "recommendation": "Prioritize local-language, high-intent keywords and refine titles, bullets, and backend terms with real search data before scaling campaigns.",
        }

    def risk_assessment(self, destination: str, product: str, constraints: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            "destination": destination,
            "product": product,
            "risk_level": "moderate",
            "risks": [
                "Local pricing and packaging may differ from the exporter’s home market.",
                "Regulatory or labeling requirements may vary by destination.",
                "Marketplace competition may be uneven across segments within the same category.",
            ],
            "mitigations": [
                "Run a localized pricing and listing test before a full inventory commitment.",
                "Confirm compliance and labeling requirements early in the product selection phase.",
                "Use differentiated bundles or product claims where the category is crowded.",
            ],
            "constraints": constraints or [],
        }

    def build_full_brief(
        self,
        destination: str,
        product: str,
        market_language: str = "en",
        target_channel: str = "Amazon",
        price_band: str = "medium",
        constraints: Optional[List[str]] = None,
        budget: Optional[str] = None,
        notes: str = "",
    ) -> Dict[str, Any]:
        constraints = constraints or []
        trends = self.market_trends(destination, product, market_language, constraints, budget)
        entry = self.market_entry(destination, product, target_channel, constraints, budget)
        opportunity = self.product_opportunity(destination, product, price_band, constraints)
        seo = self.sku_seo(destination, product, market_language, target_channel)
        risks = self.risk_assessment(destination, product, constraints)

        report_markdown = "\n\n".join([
            f"# Detailed market report: {product} in {destination}",
            f"## Executive summary\n{trends['headline']}",
            f"## Trend analysis\n{trends['analysis']}",
            f"## Platform fit\n{entry['recommendation']}",
            f"## Product opportunity\n{opportunity['why_it_works']}",
            f"## SEO plan\n{seo['recommendation']}",
            f"## Risk assessment\n{risks['risks'][0]}",
            f"## Notes\n{notes or 'No extra notes provided.'}",
        ])

        return {
            "destination": destination,
            "product": product,
            "market_language": market_language,
            "target_channel": target_channel,
            "price_band": price_band,
            "constraints": constraints,
            "budget": budget or "not specified",
            "notes": notes,
            "summary": {
                "headline": trends["headline"],
                "winner": entry["recommendation"],
                "opportunity_score": opportunity["opportunity_score"],
            },
            "trend_analysis": trends,
            "platform_recommendation": entry,
            "product_opportunity": opportunity,
            "seo_plan": seo,
            "risk_assessment": risks,
            "data_gaps": {
                "search_volume": "Requires live validation",
                "category_ranking": "Requires marketplace ranking checks",
                "pricing": "Needs local price benchmarking",
            },
            "report_markdown": report_markdown,
            "final_note": "This recommendation is directional; validate with live search, marketplace, and keyword data before committing inventory or ad spend.",
        }
