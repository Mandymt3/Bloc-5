FROM continuumio/miniconda3

COPY . /home/app

RUN pip install -r /home/app/requirements.txt


# run the mlflow server in the container
CMD mlflow server -p $PORT \
    --host 0.0.0.0 \
    --backend-store-uri $BACKEND_STORE_URI \
    --default-artifact-root $ARTIFACT_ROOT
