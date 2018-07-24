# System Overview 

Overview of AdvEx's system architecture.

## Frontend

- Frontend is consisted of 6 pages: sign-up, log-in, dashboard (where the user can upload a model for evaluation), submission history page, submission detail page and info page (including disclaimer, submission instructions, explainations of attack methods and evaluation dataset).
- Use Vue.js due to its similarity and superiority (reactivity + components) to Angular.js.
- Use [Apiary](apiary.io) to simulate API responses, so as to develop independently from backend.
- Model (.h5) and index (.json) files are directly uploaded to S3. The actual files are never transmitted in the request. Instead, the S3 keys will indicate where to retrieve the files.

## Backend

- Use Python and Flask.
- Provide APIs for frontend to use.
- Forward evaluation tasks to workers by pushing them to Simple Queue Service (SQS).
- Interact with AWS RDS (engine: PostgreSQL) through SQLAlchemy.
- Write unit tests for APIs and DB interaction.
- Set up with Travis CI for continuous integration.
- Use Postman to test the APIs from the frontend's perspective.
- APIs are documented in `API.md`. Sign up with [Apiary](apiary.io) and copy the file into the editor to use it.

## Evaluation

- Use Python.
- Pull tasks from SQS. If no task is present, sleep for a duration of time.
- Evaluate the task and write feedback into DB.
- The evaluation algorithm can be modified independently from the system.

## Integration & Deployment

- Components will be dockerized and deployed with Elastic Beanstalk.
- Need to carefully configurate credentials and communication channels (host, port, etc)
- Load balancing and auto scaling have in-house support from Elastic Beanstalk.
