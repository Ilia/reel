# Reel Project

TLDR - Exploring SAM with Python

![example workflow](https://codebuild.ap-southeast-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiRXIwMldGT1BCbW9idVNHbUx6dFVxbTh1bnozVnRES0M3Ni9NbUtNeHFhUHkzcTRjR2JvWk12YnVXUncraklxSWJtTlJKWDBCZE1xNmMwQmwzdURibGFjPSIsIml2UGFyYW1ldGVyU3BlYyI6IjIwQnpSREk2OUs4dlBqWlgiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

## The Problem

We need to grab reel information from the SlateAPP API, but the response time from the API end points is not performant and since the data from that API doesn't change much, we need a caching mechanism in between - this is where this mini project comes in. 

## The Solution

Let's go serverless! 

What we need is a simple API to connect to and get the reels information fast! We also want to be able to tell this API to cache the data either thru user action or on schedule (daily).

This project provide 2 entry points:
1. /reel/{id} - which will get you the cache reel information or will get the reel information in real-time (pass thru) if the data is not available in cache
2. /cache - which will cache all the reel data 

The solution will use the following technologies:

1. SAM
2. Lambda  
3. API Gateway
4. SNS 
5. DynomoDB
6. SSM
7. Cognito
8. SES - (see TODO)
9. Cloud Watch (see TODO)
10. CodeBuild

Yes - there is probably better ways to do this, and potentially even get API Gateway to cache, but this is an education related project, where I am trying to familiarise myself with all AWS. 

## TODO
- [x] Figure out how to properly structure project
- [x] Find out how to use request library, which Lambda doesn't have
- [x] Find out how to add API Gateway
- [x] Update Dynomodb
- [x] Workout how to get SSM working to remove API Key from variable/repo
- [x] Finish DynomoDB integration via SAM template
- [x] Work out how to monitor SNS Topic, and consumption of messages
- [x] getReel, workout how to handle cache for items not in DynomoDB (invoke lambda? Or is there better?)
- [x] Add Cognito to API Gateway, so only auth users can invoke it
- [ ] If anything goes wrong, we need to email the user (cache didn't work, etc)
- [ ] Cloud Watch event setup, so that cache is invoked at regular time
- [ ] Break template.yaml into sub template for better maintenance
- [x] Work out how to use pytest and create a unit test 
- [ ] Add tests, lots of tests 
- [x] Add various Env parameter (Prod, Stage, Dev)
- [ ] Proper use of ENV parameter (Prod, Stage, Dev)
- [ ] Add Output to template
- [x] Make LayerVersion work, need to read up on how to use it properly
- [x] CI/CD thru Github Actions
- [x] CI/CD thru CodeBuild
- [ ] Add versioning
- [x] Work out how to use Layer functions in tests
- [x] Work out how to trigger tests in CI/CD
- [ ] Cognito - find out how to setup HostedUI + App client full setup via CloudFormation/SAM
- [ ] get Reel function, handle better when no reel found

## Local Tests

To run local tests:
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r tests/requirements.txt
export PYTHONPATH=$PWD/src/library:$PWD/src:$PYTHONPATH
python3 -m pytest tests

### Tips/Tricks/Hints 

Things I need to remember:
1. export AWS_PROFILE='profile' before running sam deploy
2. SSM Parameter Store "REEL_API_KEY" should match the "Default" value
3. "is in ROLLBACK_COMPLETE state and can not be updated." - need to manual remove the stack, seems the stack is empty, but its in a state, that cannot be deployeed, there is a way to use create-stack --on-failure, but that doesn't work with deploy.
4. You can view all logs related to Lambda via lambda/home -> Monitoring
5. To check your items in Dynomodb in the aws console UI ensure to refresh the page :)
6. Always check what Policies is required for the functions
7. "An error occurred (ExpiredToken) when calling the PutObject operation: The provided token has expired." -> export AWS_PROFILE=<profile name>

### Auth

Login:
https://reel-sample-application.auth.ap-southeast-2.amazoncognito.com/login?client_id=cp0shbd5h0chjas3pcmt4euic&response_type=token&scope=email+openid&redirect_uri=http://localhost/


### Resources

https://aws.amazon.com/blogs/compute/introducing-aws-sam-pipelines-automatically-generate-deployment-pipelines-for-serverless-applications/
https://aws.plainenglish.io/a-practical-guide-surviving-aws-sam-part-3-lambda-layers-8a55eb5d2cbe
https://hands-on.cloud/how-to-test-python-lambda-functions/

https://github.com/aws-samples/aws-serverless-workshops
https://stackoverflow.com/questions/65270647/running-pytest-in-aws-sam-doesnt-use-env-vars-in-template-yaml
https://tenmilesquare.com/resources/software-development/aws-sam-api-with-cognito/

