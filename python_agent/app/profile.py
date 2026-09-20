from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict


@dataclass
class Profile:
    facts: Dict[str, str] = field(default_factory=dict)
    notes: str = ""
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def needs_interview(self) -> bool:
        return self.facts.get("interview.completed") != "true" and self.facts.get("interview.skipped") != "true"

    def mark_interview_complete(self) -> None:
        self.facts["interview.completed"] = "true"
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def skip_interview(self) -> None:
        self.facts["interview.skipped"] = "true"
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def add_fact(self, key: str, value: str) -> None:
        self.facts[key] = value
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "facts": self.facts,
            "notes": self.notes,
            "updated_at": self.updated_at,
        }
