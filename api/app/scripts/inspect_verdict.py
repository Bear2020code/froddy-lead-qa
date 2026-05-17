from app.verdict import VerdictEngine


def main() -> None:
    engine = VerdictEngine()

    sample_actions = [
        {
            "dialogue_id": "d_002",
            "classification": "warm_lead",
            "loss_type": "brutal_loss",
            "action_type": "follow_up",
            "draft": "Здравствуйте! Подскажите, задача ещё актуальна?",
        },
        {
            "dialogue_id": "d_006",
            "classification": "conflict",
            "loss_type": "no_loss",
            "action_type": "escalate",
            "draft": "Передать человеку.",
        },
        {
            "dialogue_id": "d_010",
            "classification": "negotiation",
            "loss_type": "no_loss",
            "action_type": "follow_up",
            "draft": "Можем сделать скидку и начать завтра.",
        },
    ]

    for action in sample_actions:
        result = engine.apply(action)
        print(
            result["dialogue_id"],
            result["verdict"],
            result["verdict_rule_id"],
            "-",
            result["verdict_reason"],
        )


if __name__ == "__main__":
    main()
