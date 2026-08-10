import json
import os
import uuid

import boto3


s3_client = boto3.client("s3")

UPLOAD_BUCKET = os.environ["UPLOAD_BUCKET"]

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png"
}

MAX_URL_EXPIRATION = 300


def lambda_handler(event, context):
    try:
        body = parse_request_body(event)

        file_name = body.get("file_name")
        content_type = body.get("content_type")

        if not file_name:
            return create_response(
                400,
                {"message": "file_name is required"}
            )

        if not content_type:
            return create_response(
                400,
                {"message": "content_type is required"}
            )

        if content_type not in ALLOWED_CONTENT_TYPES:
            return create_response(
                400,
                {
                    "message": (
                        "Unsupported file type. "
                        "Only JPEG and PNG images are allowed."
                    )
                }
            )

        file_extension = ALLOWED_CONTENT_TYPES[content_type]

        object_key = (
            f"uploads/{uuid.uuid4()}{file_extension}"
        )

        presigned_url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": UPLOAD_BUCKET,
                "Key": object_key,
                "ContentType": content_type
            },
            ExpiresIn=MAX_URL_EXPIRATION
        )

        return create_response(
            200,
            {
                "upload_url": presigned_url,
                "object_key": object_key,
                "expires_in": MAX_URL_EXPIRATION
            }
        )

    except Exception as error:
        print(f"Failed to generate presigned URL: {error}")

        return create_response(
            500,
            {
                "message": "Unable to generate upload URL"
            }
        )


def parse_request_body(event):
    body = event.get("body")

    if body is None:
        return {}

    if isinstance(body, dict):
        return body

    return json.loads(body)


def create_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }