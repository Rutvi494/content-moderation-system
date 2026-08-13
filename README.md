## Day 5 - React Image Moderation Interface

Built a React frontend for the image moderation workflow.

### Features

- JPEG and PNG image selection
- Client-side file validation
- Image preview
- Secure direct upload to Amazon S3 using presigned URLs
- Image moderation through Amazon Rekognition
- APPROVE, REVIEW, and BLOCK decisions
- Moderation confidence display
- Error and loading states

### Frontend Flow

React
→ API Gateway
→ Presigned URL Lambda
→ Amazon S3
→ Moderation API
→ Amazon Rekognition
→ DynamoDB
→ React moderation result