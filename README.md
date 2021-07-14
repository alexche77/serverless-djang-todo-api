
# Trying out serverless Django with Zappa

  
  
  

## About local development

  

This project is setup with Docker and docker-compose. Basically it runs the app container, with our code, based on this image lambci/lambda:build-python3.8 and a postgresql container based on official docker image.

  
  

**To run this code you will need:**

  

- Docker and Docker compose



# Initial setup

1. Make sure to copy .env.example to .env to start filling out your **local** environment variables.

2. Create a virtual env locally on your machine (we do this so VS Code can find our dependencies)

	- `python3 -m venv env` # Create the actual environment

	- `source ./env/bin/activate` # Activates the newly created env

3. Install dependecies:
	- `pip install --upgrade pip` # Updates pip to latest version (Always do this)

	- `pip install -r requirements.txt` # Installs dependencies based of our requirements.txt

4. Build and run the image for your project:
	- Run `docker-compose build` to build the images

	- Run `docker-compose up` to run the project

	This will run the project, instantiate the database, create it, run 'wait_for_db' command on the app container and run migrate command too.

5. Check your project is running:
	- Go to localhost:8000 on your browser and you should see your app running 

6. Create the super user:
	**NOTE: Make sure to set all your environment variables before running this.**
	
	`docker compose exec app sh -c 'python3 manage.py createsuperuser --noinput'`
	
	This command executes the createsuperuser manage command in non-interactive mode. 

7. Go to /admin and try to login, it should work.

# About lambci/lambda:build-python3.8

This image is as close as it can to AWS Lambda environment, so, if our code runs well within that container, then it means that it will work on actual AWS Lambda.


# Deploying with zappa

TODO: Thingking about expanding this guide
TODO: Add steps to create zappa utility user on AWS console

**For this part, we asume you have created a zappa user and have configured your aws_credentials and zappa profile**

1. Run `zappa init` and answer the questions. After running this, zappa would have created a couple of files.
2. Go into zappa_settings.json, and specify region inside the environment you wish to deploy, otherwise it will fail.
3. Update `zappa_settings.json.[env].django_settings` key to `"app.settings"` otherwise it will fail when you deploy it.
3. Move zappa_settings.json to the app subfolder
4. Deploy with `zappa deploy [env]`