FORMAT: 1A

# AdvEx

API documentation of AdvEx's backend.

## User [/users]

+ Attributes (object)
    + user_id: 1 (required, string)
    + email: dave@gmail.com (required, string)
    + nickname: Dave (required, string)

### Register a new user [POST]

+ Attributes (object)
    + email: dave@gmail.com (required, string)
    + nickname: Dave (required, string)
    + password: aircrash (required, string)

+ Request (application/json)

+ Response 200

### Get information of a user [GET /users/{user_id}]

+ Parameters
    + user_id: 1 (required, string) - ID of the user

+ Response 200 (application/json)
    + Attributes (User)

### Get submission history of a user [GET /user/{user_id}/submissions]

+ Parameters
    + user_id: 1 (required, string) - ID of the user

+ Response 200 (application/json)
    + Attributes (object)
        + submission_ids: 1, 2, 3 (required, array[string])

## Submission [/submissions/{submission_id}]

+ Parameters
    + submission_id: 1 (required, string) - ID of the submission

+ Attributes (object)
    + submission_id: 1 (required, string)
    + user_id: 1 (required, string)
    + s3_model_key: 7796f75c-f8f5-4707-901d-edcca3599326 (required, string)
    + s3_json_key: 7796f75c-f8f5-4707-901d-edcca3599326 (required, string)
    + created_at: 2014-11-11T08:40:51.620Z (required, string)

### Get detail of a submission [GET]

+ Response 200 (application/json)
    + Attributes (Submission)

### Update feedback of a submission [POST]

+ Attributes (object)
    + submission_id: 1 (required, string)
    + feedback (required, object)
        + score: 0.99 (required, number)
        + img_urls: dummy.com/1.jpg, dummy.com/2.jpg (required, array[string])

+ Response 200

## Misc [/]

### Log in [POST /login]

+ Attributes (object)
    + email: dave@gmail.com (required, string)
    + password: aircrash (required, string)

+ Request (application/json)

+ Response 200

+ Response 401

### Log out [POST /logout]

+ Response 200

### Submit a model to evaluate [POST /submit]

+ Attributes (object)
    + user_id: 1 (required, string)
    + s3_model_key: `7796f75c-f8f5-4707-901d-edcca3599326` (required, string)
    + s3_json_key: 7796f75c-f8f5-4707-901d-edcca3599326 (required, string)

+ Request (application/json)

+ Response 200 (application/json)
    + Attributes (object)
        + submission_id: 1 (required, string)
