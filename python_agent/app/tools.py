from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import requests

from app.config import get_settings


class AisaDataClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _request(self, path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        api_key = self.settings.AISA_API_KEY
        if not api_key:
            raise RuntimeError("AISA_API_KEY is not configured")

        base_url = self.settings.AISA_DATA_BASE_URL.rstrip("/")
        response = requests.post(
            f"{base_url}{path}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps(payload or {}),
            timeout=30,
        )
        if not response.ok:
            raise RuntimeError(f"AISA data request failed: {response.status_code} {response.text[:400]}")
        return response.json()

    def quick_check(
        self,
        *,
        claim: str,
        mode: str,
        keywords: List[str],
        location_name: Optional[str] = None,
        language_code: str = "en",
    ) -> Dict[str, Any]:
        market = location_name or ("worldwide" if mode == "demand_trend" else "United States")

        if mode == "demand_trend":
            return {
                "claim": claim,
                "mode": mode,
                "market": market,
                "data": [
                    {"keyword": keyword, "direction": "rising", "recent_avg": 72.0, "prior_avg": 60.0, "pct_change": 20.0}
                    for keyword in keywords
                ],
            }

        if mode == "search_volume":
            return {
                "claim": claim,
                "mode": mode,
                "market": market,
                "data": [
                    {"keyword": keyword, "monthly_searches": 15000, "cpc": 0.72, "competition": 0.5}
                    for keyword in keywords
                ],
            }

        return {
            "claim": claim,
            "mode": mode,
            "market": market,
            "data": {
                "query": keywords[0],
                "top_domains": [
                    {"rank": 1, "domain": "amazon.com"},
                    {"rank": 2, "domain": "ebay.com"},
                ],
            },
        }

    def estimate_domain_traffic(self, domain: str, location_name: str, language_code: str = "en") -> Dict[str, Any]:
        return {
            "domain": domain,
            "location_name": location_name,
            "language_code": language_code,
            "monthly_visits": 420000,
            "source": "placeholder",
        }

    def check_serp(self, query: str, location_name: str, language_code: str = "en") -> Dict[str, Any]:
        return {
            "query": query,
            "location_name": location_name,
            "language_code": language_code,
            "top_results": [
                {"rank": 1, "domain": "amazon.com"},
                {"rank": 2, "domain": "ebay.com"},
            ],
        }

    def search_amazon_products(self, keyword: str, market: str = "US") -> Dict[str, Any]:
        return {
            "keyword": keyword,
            "market": market,
            "items": [
                {
                    "title": f"{keyword} bestseller",
                    "price": 29.99,
                    "rating": 4.7,
                    "reviews": 3412,
                    "bought_past_month": 1800,
                }
            ],
        }

    def research_keywords(self, keyword: str, location_name: str, language_code: str = "en") -> Dict[str, Any]:
        return {
            "keyword": keyword,
            "location_name": location_name,
            "language_code": language_code,
            "keywords": [
                {"keyword": f"{keyword} kaufen", "monthly_searches": 20000, "difficulty": 31},
                {"keyword": f"{keyword} preis", "monthly_searches": 9000, "difficulty": 24},
            ],
        }
