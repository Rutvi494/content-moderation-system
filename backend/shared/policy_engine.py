def make_image_decision(labels):
    block_categories = {
        "Explicit Nudity",
        "Sexual Activity",
        "Graphic Violence"
    }

    review_categories = {
        "Suggestive",
        "Violence",
        "Weapons",
        "Drugs"
    }

    highest_confidence = 0

    for label in labels:
        confidence = float(
            label["confidence"]
        )

        highest_confidence = max(
            highest_confidence,
            confidence
        )

        if (
            label["name"] in block_categories
            and confidence >= 85
        ):
            return (
                "BLOCK",
                round(confidence / 100, 2),
                (
                    f'{label["name"]} detected '
                    f'with {confidence}% confidence'
                )
            )

    for label in labels:
        confidence = float(
            label["confidence"]
        )

        if (
            label["name"] in review_categories
            and confidence >= 60
        ):
            return (
                "REVIEW",
                round(confidence / 100, 2),
                (
                    f'{label["name"]} detected '
                    f'with {confidence}% confidence'
                )
            )

    return (
        "APPROVE",
        round(highest_confidence / 100, 2),
        "No prohibited moderation category detected"
    )