FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

ADD ./requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt
COPY ./app /app
COPY ./db /db
