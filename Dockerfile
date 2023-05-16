FROM python:3.10.11-slim

COPY ./app /app
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# set working directory
WORKDIR /app

# expose port
EXPOSE 80

# run server
CMD ["python3", "main.py"]

