# Content Moderation Test Results

| Test ID | Image | Expected | Actual | Label | Confidence | Result |
|---|---|---|---|---|---|---|
| T1 | test-image.jpg | APPROVE | APPROVE | None | 0% | PASS |
| T2 | weapen.jpg | APPROVE | APPROVE | None | 0% | PASS |
| T3 | gun.jpg | REVIEW | REVIEW | Weapons | 94% | PASS |


## Summary

Total tests: 9
Passed: 8
Failed: 1

### Observations

- Safe landscape and food images were approved.
- A toy-weapon image triggered the Weapons moderation category.
- Unsupported files were rejected before upload.
- Invalid S3 object keys returned HTTP 400.
- Successful moderation records were stored in DynamoDB.
- Failed moderation requests were not persisted.

### Known Issues

- One expected REVIEW image was classified as APPROVE.
- Additional moderation examples are needed before changing thresholds.