from backend.shared.policy_engine import make_image_decision


def test_safe_image():
    labels = []

    decision, risk, reason = make_image_decision(labels)

    assert decision == "APPROVE"
    assert risk == 0


def test_weapon_requires_review():
    labels = [
        {
            "name": "Weapons",
            "parent_name": "Violence",
            "confidence": 80,
        }
    ]

    decision, risk, reason = make_image_decision(labels)

    assert decision == "REVIEW"
    assert risk == 0.8


def test_high_confidence_explicit_content():
    labels = [
        {
            "name": "Explicit Nudity",
            "parent_name": "Nudity",
            "confidence": 95,
        }
    ]

    decision, risk, reason = make_image_decision(labels)

    assert decision == "BLOCK"
    assert risk == 0.95