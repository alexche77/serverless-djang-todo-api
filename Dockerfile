FROM lambci/lambda:build-python3.8

# Make this the default working directory
WORKDIR /var/task
COPY ./app /var/task

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# Expose tcp network port 8000 for debugging
EXPOSE 8000

 

# Fancy prompt to remind you are in zappashell
RUN echo 'export PS1="\[\e[36m\]zappashell>\[\e[m\] "' >> /root/.bashrc