# System Overview 

Overview of AdvEx's system architecture.

## Frontend

- Frontend is basically consisted of 4 pages: sign-up, log-in, dashboard (where the user can submit a model and browse his submission history) and submission detail page.
- Plan to use Vue.js due to its similarity and superiority (reactivity + components) to Angular.js.
- Use [Apiary](apiary.io) to simulate API responses, so as to develop independently from backend.
- Model and mapping (JSON file) is directly uploaded to S3 at frontend. The actual file is never transmitted in the request. Instead, the S3 keys will indicate where to retrieve the files.
- Use polling to incrementally retrieve the feedback.

## Backend

- Plan to use Python and Flask.
- Provide APIs for frontend and workers to use.
- Forward evaluation tasks to workers by pushing them to Simple Queue Service (SQS).
- Interact with AWS RDS (engine: PostgreSQL) through SQLAlchemy.
- Write unit tests for APIs and DB interaction.
- Use Postman to test the APIs from the frontend's perspective.
- APIs are documented in `API.md`. Sign up with [Apiary](apiary.io) and copy the file into the editor to use it.

## Evaluation

- Work in an infinite loop.
- Pull tasks from SQS. If no task is present, sleep for a duration of time.
- Evaluate the task and write feedback into DB (either call backend's API or write directly).
- Generate the sample images and upload them to S3.
- The evaluation algorithm can be modified independently from the system.

## Integration & Deployment

- Components will be dockerized and exported to AMIs.
- Need to carefully configurate credentials and communication channels (host, port, etc)
- Use Auto-scaling Group (ASG) for the workers and scale it based on the queue length of SQS.
