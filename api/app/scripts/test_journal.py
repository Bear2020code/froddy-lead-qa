from app.journal import append_decision, clear_decisions, list_decisions


def main() -> None:
    clear_decisions()

    record = append_decision(
        {
            "dialogue_id": "d_test",
            "manager_name": "Test Manager",
            "original_verdict": "review",
            "human_decision": "allow",
            "action_type": "follow_up",
            "verdict_rule_id": "test_rule",
        }
    )

    if record["dialogue_id"] != "d_test":
        raise AssertionError("Journal record was not written correctly.")

    items = list_decisions()

    if len(items) != 1:
        raise AssertionError(f"Expected 1 journal item, got {len(items)}.")

    if items[0]["human_decision"] != "allow":
        raise AssertionError("Journal item has wrong human decision.")

    clear_decisions()

    if list_decisions():
        raise AssertionError("Journal was not cleared.")

    print("Journal tests passed")


if __name__ == "__main__":
    main()
