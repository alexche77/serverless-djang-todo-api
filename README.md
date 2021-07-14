# Trying out serverless Django with Zappa



## About local development

This project is setup with Docker and docker-compose. Basically it runs the app container, with our code, based on this image lambci/lambda:build-python3.8 and a postgresql container based on official docker image.


To run this code you will need:

- Docker and Docker compose
- Create a virtual env locally on your machine (we do this so VS Code can find our dependencies)
    python3 -m venv env   # Create the actual environment
    source ./env/bin/activate # Activates the newly created env
    pip install --upgrade pip # Updates pip to latest version (Always do this)
    pip install -r requirements.txt # Installs dependencies based of our requirements.txt
- Run docker-compose build to build the images
- Run docker-compose up to run the project
    This will run the project, instantiate the database, create it, run 'wait_for_db' command on the app container
    and run migrate command too.
- Go to localhost:8000 on your browser and you should see your app running
    


# About lambci/lambda:build-python3.8

This image is as close as it can to AWS Lambda environment, so, if our code runs well within that container, then it means that it will work on actual AWS Lambda.


