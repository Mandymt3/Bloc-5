docker run -it^
 -v "C:\Data learning\Jedha\Fullstack\Project\6.Deployment\Getaround_API:/home/app"^
 -p 4030:4030^
 -e PORT=4030^
 -e AWS_ACCESS_KEY_ID="AKIA3DPV47ID2J7XQ2YJ"^
 -e AWS_SECRET_ACCESS_KEY="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"^
 -e BACKEND_STORE_URI="postgresql://bwwjycdkvdeoax:bc3244c33369af38615be00b50bc326d1630cc580739ba3c9408b5da2c3fd133@ec2-54-204-56-171.compute-1.amazonaws.com:5432/dejgcvuprlpsgs"^
 -e ARTIFACT_ROOT="s3://cours-demo"^
 -e MLFLOW_TRACKING_URI="https://getaround-mlflow-server.herokuapp.com/"^
 getaround-api 