# AdvEx Deployment Instructions

## Disclaimer

This document is intended for developers with basic understanding of Web development and Amazon Web Services. We recommend the following resources if you need some catch-up materials:

- [Web Technology for Developers](https://developer.mozilla.org/en-US/docs/Web)
- [Getting Started on Amazon Web Services (AWS)](https://aws.amazon.com/getting-started/)

## AWS Resources Setup

### AWS Credentials Setup

As the first step, you will need to set up AWS credentials so that you can access the resources. There are various approaches to this as detailed in the [official guide](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html), but we recommend that you put the credentials in the file `~/.aws/credentials`.

In this project, you need to set up 3 fields:

- `AWS_DEFAULT_REGION`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### S3

1. Go to [Amazon S3](https://aws.amazon.com/s3/) web console.

2. Create a new Bucket. Configurate the options as needed.

3. In this bucket, create a folder named `evaluation_data`. Upload `image_data_final.zip` to that folder. Instructions about how to generate the evaluation datasets can be found [here](TODO).

4. In `AdvEx-Evaluation/src/evaluation_worker.py`, change the bucket name accordingly.

### Lambda & API Gateway

Follow this [instruction](https://github.com/dnc1994/AdvEx-FE/blob/master/docs/dropzone.md) to configurate Lambda and API Gateway, which will enable direct uploading to S3 from browser.

### SQS

1. Go to [Amazon Simple Queue Service](https://aws.amazon.com/sqs/) web console.

2. Create a new Standard Queue. Configurate the options as needed. Note that the visibility timeout should typically be increased from the default value to 30 seconds. In this project, it's safe to set it to the maximum 12 hours.

3. In `AdvEx-BE/app.py`, change the queue name accordingly.

4. Do the same in `AdvEx-Evaluation/src/evaluation_worker.py`.

### RDS

1. Go to [Amazon Relational Database Service](https://aws.amazon.com/rds) web console.

2. Create a DB instance with "PostgreSQL"as the engine.

3. Configurate the options as needed. Save the Master password for later use.

## Deployment with Elastic Beanstalk

### Initial Setup through Web Console

1. Go to [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) web console.

2. Create a new application

3. Create a new environment for the frontend.

    - Select "Web server" in environment tier.
    - Use an intuitive domain name.
    - Select "Preconfigured Docker" as platform.
    - Launch with sample code.

4. After the environment launches, go to configuration panel and change a few settings:

    - Under "Software", add the following environment variables:
        - `AWS_DEFAULT_REGION`
        - `AWS_ACCESS_KEY_ID`
        - `AWS_SECRET_ACCESS_KEY`
        - `SQLALCHEMY_DATABASE_URI`: the database URL for the RDS instance you've created. It should be in the format of `postgresql+psycopg2://<username>:<password>@<endpoint>:<port>/<database_name>`. The endpoint is available in the RDS dashboard.
    - Under "Instances", change EC2 instance type to what best fits your expected production scale.
    - Under "Capacity", change environment type from single-instance to load-balanced. Configurated the scaling rules as needed.

5. Repeat steps 3 - 4 for backend and evaluation worker. Note that for the worker you need to select "Worker" when creating the new environment.

### Configurate Domain Name

Assuming that you already own a domain name, there are several places where you need to set it:

- In line 2 of `AdvEx-FE/vue.config.js`, change `https://advex.org` to your domain name.
- In line 2 of `AdvEx-FE/src/config.js`, change `https://api.advex.org` to the `api` sub-domain of your domain name.

### Create Route 53 Records

1. Go to [Amazon Route 53](https://aws.amazon.com/route53/) web console.
2. Create a new Hosted Zone
3. Associate it with your domain name (setting up NS and SOA records). If you purchase the domain name through AWS, this part is automatically done.
4. Create an `A` record that points your domain to an "Alias Target" of the frontend environment you created with Elastic Beanstalk (it will be listed in the dropdown).
5. Similarly, create an `A` record that points the `api` sub-domain to the backend environment. 

### Enable HTTPS

1. Go to [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/) web console.
2. Request a certificate for your domain name. To validate ownership of the domain name, typically you need to edit its DNS configuration as instructed. If you purchase the domain name through AWS, this is an one-click process.
3. Do the same for the `api` sub-domain.
4. After both certificates are issued, go to configuration panel of the frontend environment in Elastic Beanstalk web console. Under "Load Balancer", add a new listener:
    - Port: 443
    - Protocol: HTTPS
    - Instance port: 80
    - Instance protocol: HTTP
    - SSL certificate: select the certificate for your domain name.
5. Do the same for the backend environment, which should use the certificate of the `api` sub-domain.

You can also find the official guide for this process [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https-elb.html).

### Deploy through EB CLI

1. Install [Elastic Beanstalk CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html)
1. Go to `AdvEx-FE` folder and run `eb init`. You will need to select region, application and environment names so that it can find the corresponding environment you've set up previously.
2. Run `eb deploy` and wait for the proccess to finish.
3. Do the same for backend and evaluation worker.
