# Simple Deployment of Machine Learning Models with Docker

## Install 
```
pip install git+https://github.com/leokster/deploy_model
```

## What is deploy_model for
**deploy_model** is a library containing tools for deploying machine learning models as REST APIs to Docker container. deploy_model installs the CLI command ```deploy-rest-api```. This command builds based on a project folder containing a scoring script and other relevant files, a Docker Image. 

## How does it work
Have a look in the [example_project](./example_project), where we have the following files:
- **score.py (required)** - This file requires at least a ```init``` and a ```run``` function. The ```init``` gets executed when the webserver starts and the ```run``` with every request. The ```init``` doesn't take any arguments, the ```run``` gets the ```flask.request.json```.
- **requirements.txt (recommended)** - Contianing the specifics of the Python environment, where the deployment should happen
- **.env (optional)** - A file containing env variables. 
- **request.py** - Does not have to be part of the package, but however you can test your deployment with this script. 


## How to use it
Given your project folder (e.g. [example_project](example_project)). You have to run 

```
deploy-rest-api --project-folder ./example_project
```

Alternatively you can also just pass the score script and requirements.txt file:

```
deploy-rest-api --requirements ./example_project/requirements.txt --score-script ./example_project/score.py
```

You will get the statement, to run the docker container as an answer from the too: e.g. 
```
docker run -p 5000:5000 deployed_model
```

## What to do with secrets
There is a more secure and a less secure way of sharing secrets with your deployment. 

### 1. Putting them into the .env file (less secure)
You can create a .env file and use the python module [python-dotenv](https://pypi.org/project/python-dotenv/) to get the environment variables. 
### 2. Passing them as envs during runtime (more secure)
Instead of just running the docker run the docker container as described above you can add environment variables:

```
docker run -p 5000:5000 --env foo=bar deployed_model
```