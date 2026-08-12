## Day 4 - Amazon API Gateway

Exposed the serverless moderation backend through an Amazon API Gateway HTTP API.

### API Endpoints

#### Generate image upload URL

POST /uploads/presigned-url

Request:

{
  "file_name": "image.jpg",
  "content_type": "image/jpeg"
}

#### Moderate uploaded image

POST /moderation/image

Request:

{
  "user_id": "user-101",
  "object_key": "uploads/image-id.jpg"
}

### Request Flow

Client
→ API Gateway
→ AWS Lambda
→ Amazon S3 / Amazon Rekognition
→ DynamoDB

CORS is enabled for development so the future React frontend can call the API.