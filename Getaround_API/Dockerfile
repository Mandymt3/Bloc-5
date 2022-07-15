FROM continuumio/miniconda3

WORKDIR /home/app

COPY . /home/app

RUN pip install -r /home/app/requirements.txt


CMD gunicorn app:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker 