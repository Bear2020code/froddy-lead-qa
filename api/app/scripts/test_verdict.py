from app.verdict import VerdictEngine


def assert_equal(actual: str, expected: str) -> None:
    if actual != expected:
        raise AssertionError(f"Expected {expected!r}, got {actual!r}")


def main() -> None:
    engine = VerdictEngine()

    allow_action = {
        "classification": "warm_lead",
        "loss_type": "brutal_loss",
        "action_type": "follow_up",
        "draft": "Здравствуйте! Задача ещё актуальна?",
    }
    assert_equal(engine.decide(allow_action).verdict, "allow")

    review_action = {
        "classification": "lost",
        "loss_type": "soft_loss",
        "action_type": "follow_up",
        "draft": "Уточню по вашему вопросу.",
    }
    assert_equal(engine.decide(review_action).verdict, "review")

    hold_action = {
        "classification": "conflict",
        "loss_type": "no_loss",
        "action_type": "escalate",
        "draft": "Нужно передать человеку.",
    }
    assert_equal(engine.decide(hold_action).verdict, "hold")

    block_action = {
        "classification": "negotiation",
        "loss_type": "no_loss",
        "action_type": "follow_up",
        "draft": "Можем сделать скидку и начать завтра.",
    }
    assert_equal(engine.decide(block_action).verdict, "block")

    print("Verdict tests passed")


if __name__ == "__main__":
    main()
