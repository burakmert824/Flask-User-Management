FROM python:3.9-slim

# set the working directory in the container
WORKDIR /app

# copy the current folder files to container
COPY . /app

# install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# make port 5001 availabe to the world outside this container
EXPOSE 5001

# define the command to run the application
ENV FLASK_APP=api_app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
