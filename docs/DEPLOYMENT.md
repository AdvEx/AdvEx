## Set up AWS Resources

### S3

### Lambda

[here](https://github.com/dnc1994/AdvEx-FE/blob/master/docs/dropzone.md).

### SQS

### RDS

## Deploy Apps on Elastic Beanstalk

### Initial Deployment through Web Console

Create app and environment through Web Console.

Select Docker and create with sample app.

Change instance type.

Switch to load balanced.

Set environment variables.

### Register a domain name



Change `AdvEx-FE/vue.config.js` and `AdvEx-FE/src/config.js`.

### Create Route 53 Records

Naked domain.

API.

### Enable HTTPS

https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https-elb.html

Add listeners.

### Deploy through EB CLI