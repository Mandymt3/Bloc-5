docker run -it^
 -v "C:\Data learning\Jedha\Fullstack\Project\6.Deployment\Getaround_mlflow:/home/app"^
 -e MLFLOW_TRACKING_URI="https://getaround-mlflow-server.herokuapp.com/"^
 -p 4020:4020^
 -e PORT=4020^
 -e AWS_ACCESS_KEY_ID="AKIA3DPV47ID2J7XQ2YJ"^
 -e AWS_SECRET_ACCESS_KEY="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"^
 -e BACKEND_STORE_URI="postgresql://jpimgxnnsdqmyw:02bc72816b474a9568c4e7a7695a3d64eada3d5c3139f57ca08cc737d7906086@ec2-44-198-82-71.compute-1.amazonaws.com:5432/ddo3qp2kdng60t"^
 -e ARTIFACT_ROOT="s3://cours-demo"^
 new-mlflow python /home/app/price_prediction.py