import json
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal

import boto3


rekognition = boto3.client("rekognition")
dynamodb = boto3.resource("dynamodb")

UPLOAD_BUCKET = os.environ["UPLOAD_BUCKET"]
MODERATION_TABLE = os.environ["MODERATION_TABLE"]

table = dynamodb.Table(MODERATION_TABLE)


def lambda_handler(event, context):
    try:
        body = parse_request_body(event)

        object_key = body.get("object_key")
        user_id = body.get("user_id", "anonymous")

        if not object_key:
            return create_response(
                400,
                {
                    "message": "object_key is required"
                }
            )

        if not object_key.startswith("uploads/"):
            return create_response(
                400,
                {
                    "message": "Invalid object key"
                }
            )

        rekognition_response = rekognition.detect_moderation_labels(
            Image={
                "S3Object": {
                    "Bucket": UPLOAD_BUCKET,
                    "Name": object_key
                }
            },
            MinConfidence=50
        )

        raw_labels = rekognition_response.get(
            "ModerationLabels",
            []
        )

        labels = normalize_labels(raw_labels)

        decision, risk_score, reason = make_decision(labels)

        moderation_id = str(uuid.uuid4())

        created_at = datetime.now(
            timezone.utc
        ).isoformat()

        item = {
            "moderation_id": moderation_id,
            "user_id": user_id,
            "content_type": "image",
            "s3_key": object_key,
            "decision": decision,
            "risk_score": Decimal(str(risk_score)),
            "reason": reason,
            "labels": labels,
            "status": get_status(decision),
            "created_at": created_at
        }

        table.put_item(
            Item=item
        )

        return create_response(
            200,
            {
                "moderation_id": moderation_id,
                "user_id": user_id,
                "content_type": "image",
                "object_key": object_key,
                "decision": decision,
                "risk_score": risk_score,
                "reason": reason,
                "labels": convert_labels_for_response(labels),
                "created_at": created_at
            }
        )

    except rekognition.exceptions.InvalidS3ObjectException:
        return create_response(
            400,
            {
                "message": (
                    "Amazon Rekognition could not access "
                    "the image in S3."
                )
            }
        )

    except Exception as error:
        print(
            f"Image moderation failed: "
            f"{type(error).__name__}: {error}"
        )

        return create_response(
            500,
            {
                "message": "Image moderation failed"
            }
        )


def parse_request_body(event):
    body = event.get("body")

    if body is None:
        return {}

    if isinstance(body, dict):
        return body

    return json.loads(body)


def normalize_labels(raw_labels):
    labels = []

    for label in raw_labels:
        labels.append(
            {
                "name": label.get("Name", ""),
                "parent_name": label.get(
                    "ParentName",
                    ""
                ),
                "confidence": Decimal(
                    str(
                        round(
                            float(
                                label.get(
                                    "Confidence",
                                    0
                                )
                            ),
                            2
                        )
                    )
                )
            }
        )

    return labels


def convert_labels_for_response(labels):
    return [
        {
            "name": label["name"],
            "parent_name": label["parent_name"],
            "confidence": float(
                label["confidence"]
            )
        }
        for label in labels
    ]


def make_decision(labels):
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


def get_status(decision):
    if decision == "REVIEW":
        return "PENDING_REVIEW"

    return "COMPLETED"


def create_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }