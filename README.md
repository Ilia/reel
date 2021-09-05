# Reel Project

TLDR - Exploring SAM with Python

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
2. Lambda functions 
3. API Gateway
4. SNS 
5. DynomoDB
6. SSM
7. Cognito - (see TODO)
8. SES - (see TODO)
9. Cloud Watch (see TODO)

Yes - there is probably better ways to do this, and potentially even get API Gateway to cache, but this is an education related project, where I am trying to familiarise myself with all AWS. 

## TODO
- [x] Figure out how to properly structure project
- [x] Find out how to use request library, which Lambda doesn't have
- [x] Find out how to add API Gateway
- [x] Update Dynomodb
- [ ] Workout how to get SSM working to remove API Key from variable/repo
- [ ] Finish DynomoDB integration via SAM template
- [ ] getReel, workout how to handle cache for items not in DynomoDB (invoke lambda? Or is there better?)
- [ ] Add Cognito to API Gateway, so only auth users can invoke it
- [ ] If anything goes wrong, we need to email the user (cache didn't work, etc)
- [ ] Cloud Watch event setup, so that cache is invoked at regular time
- [ ] Break template.yaml into sub template for better maintenance
- [ ] Add tests, lots of tests 
- [ ] Add various Env (Prod, Stage, Dev)
- [ ] Add Output to template
- [ ] Make LayerVersion work, need to read up on how to use it properly

### Tips/Tricks/Hints 

Things I need to remember:
1. export AWS_PROFILE='profile' before running sam deploy
2. SSM Parameter Store "REEL_API_KEY" should match the "Default" value
3. "is in ROLLBACK_COMPLETE state and can not be updated." - need to manual remove the stack, seems the stack is empty, but its in a state, that cannot be deployeed, there is a way to use create-stack --on-failure, but that doesn't work with deploy.