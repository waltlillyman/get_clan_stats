# syntax=docker/dockerfile:1
FROM python:slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy python files into the working dir of the container:
COPY *.py ./

# When the container is run, execute this python script:
ENTRYPOINT ["python","get_clan_stats.py"]
