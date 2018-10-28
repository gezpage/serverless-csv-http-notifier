# JSON Notifier

Built using the [Serverless](https://serverless.com) application framework.

## Overview

This Lambda function is created using the Serverless application framework that provides the following flow when 
fully deployed:

- UTF-8 text file is uploaded to a specified S3 bucket containing CSV data (must have a .csv file extension)
- Lambda Python 3.5 function is triggered
- The handler code is called, which uses the boto3 library to retrieve the S3 file contents as a string value
- It is then transformed into a number of JSON strings 
- For each JSON string an HTTP POST is made to a specified endpoint with JSON as the request body
- Processing is complete once all the files are processed and all HTTP requests are made

## Usage

### Prerequisites

- Make sure python3 and pipenv are installed
- Ensure your AWS credentials are 
[configured for boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration)
- Install Serverless: `npm install -g serverless`
- Install npm Serverless dependencies in the project dir: `npm install`
- Install pip project libraries: `pipenv install`

### Configuration

In `serverless.yml` you can set the HTTP POST endpoint that the application will send to in:

    function > notifier > handler > environment > http_endpoint
    
By default this is set to use the https://httpbin.org HTTP sink for testing.

You will also find the S3 bucket name that *must* be changed to avoid a collision with an existing bucket:

    function > notifier > handler > events > s3 > bucket
    
### Deploy

You will need to deploy before you start testing as the S3 bucket will be created, that you need to test:

    sls deploy

### Testing

Test event json files can be found in `data/json`. To use these you will need to *ensure the bucket and filenames are 
correct in the JSON*, and that you have uploaded the test file to your S3 bucket (Test CSV data can be found in 
`data/testdata.csv`).

Now you can use the local event files to test locally with:

    sls invoke local -f notifier --path data/json/success.json
    
To run the tests against the lambda function, just remove the local parameter:

    sls invoke -f notifier --path data/json/success.json
    
## Logging

The handler script logs each step of the process, which becomes available in AWS CloudWatch. It uses the “Info” log 
level which gives a reasonable view on actions and errors. Enabling “Debug” will make a lot of lower level log data 
available.

Viewing the logs can be done with:

    sls logs
    
(or view logs in the CloudWatch console)

## Error Handling

Exceptions are used where possible. To prevent failures from causing the application to break before processing is 
finished, exceptions are handled and logged, and then processing continues. The main handler response will be 200 on 
complete success, or in the event of any failures during the process, it will return 500.

## Tests

Unit tests can be found in the `tests` folder, to run them use:

    python -m unittest -v tests/*
    
In order to invoke the solution locally, without deploying to AWS, you are able to use the “data/json/testdata.json” 
file with the serverless invoke subcommand. You will need a valid S3 bucket and file to already exist, and update the file 
with these details. There are examples of invalid S3 files, which is useful for testing for failure handling.

## Future Improvements

- Move uploaded files to “processed” or “failed” buckets or folders after processing
- Look at replacing Python Requests with a more performant HTTP library, perhaps PyCurl
- Look into using Placebo / moto for boto testing
- Enrich tests with data provider or test data factory
- Attempt to minimise size of zip package
- Performance benchmarking at scale if needed
- Look into standardising Python project layout
- Unsure if leaving the per-file `__main__` tests are a good idea - but useful for development
- If needed, allow for different CSV schema types; single quoted values / no quotes / different line endings etc.
- Refactor to allow for different data sources / triggers

## Considerations for Production Usage

- Is the 1 second lambda cold-start penalty a concern?
- Configure CloudWatch to alert on errors
- Investigate implications of enabling full debug level logging
- Lock down pipfile versions
- Remove dev / testing dependencies before deploy
- Restrict S3 permissions in serverless.yml
- Set up CI deployment pipeline
- Look into dead letter queues for failures
