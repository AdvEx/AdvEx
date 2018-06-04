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
        + submissions: (array[Submission])

## Submission [/submissions/{submission_id}]

+ Parameters
    + submission_id: 1 (required, string) - ID of the submission

+ Attributes (object)
    + submission_id: 1 (required, string)
    + user_id: 1 (required, string)
    + model_name: `VGG-16 v1.0` (required, string)
    + status: `submitted` (required, string) - One of [submitted, running, finished]
    + created_at: `2018-05-01T08:40:51.620Z` (required, string)

### Get detail of a submission [GET]

+ Response 200 (application/json)
    + Attributes (object)
        + submission_id: 1 (required, string)
        + user_id: 1 (required, string)
        + model_name: `VGG-16 v1.0` (required, string)
        + status: `submitted` (required, string) - One of [submitted, running, finished]
        + created_at: `2018-05-01T08:40:51.620Z` (required, string)
        + feedback (required, object) - Refer to sample feedback JSON

### Update feedback of a submission [POST]

+ Attributes (object)
    + submission_id: 1 (required, string)
    + feedback (required, object) - Refer to sample feedback JSON

+ Response 200

## Misc [/]

### Log in [POST /login]

+ Attributes (object)
    + email: dave@gmail.com (required, string)
    + password: aircrash (required, string)

+ Request (application/json)

+ Response 200
    + Attributes (object)
        + user_id: 1 (required, string)

+ Response 401

### Log out [POST /logout]

+ Response 200

### Submit a model to evaluate [POST /submit]

+ Attributes (object)
    + user_id: 1 (required, string)
    + model_name: `VGG-16 v1.0` (required, string)
    + s3_model_key: `7796f75c-f8f5-4707-901d-edcca3599326` (required, string)
    + s3_json_key: `7796f75c-f8f5-4707-901d-edcca3599327` (required, string)

+ Request (application/json)

+ Response 200 (application/json)
    + Attributes (object)
        + submission_id: 1 (required, string)
