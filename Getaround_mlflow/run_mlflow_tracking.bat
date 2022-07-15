docker run -it^
 -v "C:\Data learning\Jedha\Fullstack\Project\6.Deployment\Getaround_mlflow:/home/app"^
 -e MLFLOW_TRACKING_URI="https://getaround-mlflow-server.herokuapp.com/"^
 -p 4020:4020^
 -e PORT=4020^
 -e AWS_ACCESS_KEY_ID=""^
 -e AWS_SECRET_ACCESS_KEY=""^
 -e BACKEND_STORE_URI=""^
 -e ARTIFACT_ROOT="s3://cours-demo"^
 new-mlflow python /home/app/price_prediction.py