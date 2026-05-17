from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


DECISION_PRIORITY = {
    "allow": 0,
    "review": 1,
    "hold": 2,
    "block": 3,
}


@dataclass(frozen=True)
class DecisionVerdict:
    verdict: str
    verdict_reason: str
    rule_id: str


class VerdictEngine:
    """Deterministic V0.1 verdict engine.

    It decides whether a recommended action can be allowed,
    needs human review, must be held, or must be blocked.
    """

    def __init__(self, rules_path: str | Path | None = None) -> None:
        self.rules_path = Path(rules_path) if rules_path else self._default_rules_path()
        self.rules_text = self.rules_path.read_text(encoding="utf-8") if self.rules_path.exists() else ""

    def decide(self, action: dict[str, Any]) -> DecisionVerdict:
        classification = str(action.get("classification", "")).lower()
        loss_type = str(action.get("loss_type", "")).lower()
        action_type = str(action.get("action_type", "")).lower()
        evidence = str(action.get("evidence", "")).lower()
        draft = str(action.get("draft", "")).lower()
        seller_text = str(action.get("seller_text", "")).lower()

        text = " ".join([classification, loss_type, action_type, evidence, draft, seller_text])

        if self._contains_unsafe_seller_promise(text):
            return DecisionVerdict(
                verdict="block",
                verdict_reason="Dialogue contains an unsafe seller promise: discount, price concession or unapproved deadline.",
                rule_id="unsafe_seller_promise",
            )

        if classification == "conflict" or action_type == "escalate":
            return DecisionVerdict(
                verdict="hold",
                verdict_reason="Conflict context: automatic follow-up may worsen the situation.",
                rule_id="conflict_requires_hold",
            )

        if loss_type in {"soft_loss", "no_next_step"}:
            return DecisionVerdict(
                verdict="review",
                verdict_reason="Follow-up needs human check because context is incomplete.",
                rule_id="incomplete_context_requires_review",
            )

        if classification in {"lost", "negotiation"}:
            return DecisionVerdict(
                verdict="review",
                verdict_reason="Dialogue context is ambiguous and needs human decision.",
                rule_id="ambiguous_context_requires_review",
            )

        if action_type == "follow_up":
            return DecisionVerdict(
                verdict="allow",
                verdict_reason="Standard soft follow-up is safe.",
                rule_id="standard_follow_up_allowed",
            )

        return DecisionVerdict(
            verdict="review",
            verdict_reason="No explicit allow rule matched; human review is required.",
            rule_id="default_review",
        )

    def apply(self, action: dict[str, Any]) -> dict[str, Any]:
        decision = self.decide(action)

        enriched = dict(action)
        enriched["verdict"] = decision.verdict
        enriched["verdict_reason"] = decision.verdict_reason
        enriched["verdict_rule_id"] = decision.rule_id

        return enriched

    @staticmethod
    def _contains_unsafe_seller_promise(text: str) -> bool:
        unsafe_markers = [
            "discount",
            "скидк",
            "дешевле",
            "снизим",
            "уступим",
            "зафиксирую цену",
            "начнем завтра",
            "начнём завтра",
            "приедем завтра",
            "сделаем завтра",
            "без согласования",
            "unsafe seller promise",
        ]
        return any(marker in text for marker in unsafe_markers)

    @staticmethod
    def _default_rules_path() -> Path:
        return Path(__file__).resolve().parents[3] / "configs" / "verdict_rules.yaml"
