from app.privacy import mask_pii


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"Expected {expected!r} in {text!r}")


def assert_not_contains(text: str, forbidden: str) -> None:
    if forbidden in text:
        raise AssertionError(f"Did not expect {forbidden!r} in {text!r}")


def main() -> None:
    source = (
        "Позвоните +7 999 123-45-67, email test@example.com, "
        "сайт https://example.com/order, машина А123ВС77."
    )

    masked = mask_pii(source)

    assert_contains(masked, "[PHONE]")
    assert_contains(masked, "[EMAIL]")
    assert_contains(masked, "[URL]")
    assert_contains(masked, "[CAR_PLATE]")

    assert_not_contains(masked, "+7 999 123-45-67")
    assert_not_contains(masked, "test@example.com")
    assert_not_contains(masked, "https://example.com/order")
    assert_not_contains(masked, "А123ВС77")

    print("PII tests passed")


if __name__ == "__main__":
    main()
