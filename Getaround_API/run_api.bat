docker run -it^
 -v "C:\Data learning\Jedha\Fullstack\Project\6.Deployment\Getaround_API:/home/app"^
 -p 4030:4030^
 -e PORT=4030^
 -e AWS_ACCESS_KEY_ID=""^
 -e AWS_SECRET_ACCESS_KEY=""^
 -e BACKEND_STORE_URI=""^
 -e ARTIFACT_ROOT="s3://cours-demo"^
 -e MLFLOW_TRACKING_URI="https://getaround-mlflow-server.herokuapp.com/"^
 getaround-api 