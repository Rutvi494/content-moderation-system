# Design a Content Moderation System Using AI

An AWS-based AI content moderation system that analyzes user-generated
text and images and classifies content as:

- APPROVE
- REVIEW
- BLOCK

## Week 1 Scope

The first milestone focuses on image moderation using:

- Amazon S3
- AWS Lambda
- Amazon Rekognition
- Amazon DynamoDB
- Amazon API Gateway

## Planned Workflow

1. The user selects an image.
2. The application generates a presigned S3 upload URL.
3. The image is uploaded to a private S3 bucket.
4. Amazon Rekognition analyzes the image.
5. A policy engine returns APPROVE, REVIEW, or BLOCK.
6. The moderation result is stored in DynamoDB.