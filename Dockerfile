FROM btobias92/rpi-base-py:latest

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "web.py"]