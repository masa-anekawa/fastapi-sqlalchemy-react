FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

ADD ./requirements.txt ./requirements.txt
RUN python -m pip install -r ./requirements.txt

# COPY ./app ./app
# COPY ./db ./db
