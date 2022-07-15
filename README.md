# Project Deployment 
## Project Getaround Analysis
### Description 
When using Getaround, it happens from time to time that drivers are late for the checkout. Late returns at checkout generate users unsatisfied even with the cancelation of rental.
This project has 2 purposes:
- To solve the late checkout issue by implementing a threshold of minimum delay minutes and scope of check flow
- To create an API that allows getting prediction of the rental price 
### Dataset
File get_around_delay_analysis.xlsx is provided by Jedha to analyze the late checkout issue
File get_around_pricing_project.csv is provided by Jedha to predict daily rental price 
### Usage
Folder **Getaround_analyse** produced a web dashboard showing some data visualizations
Folder **Getaround_mlflow** produced a web that allows tracking ML training, metrics and parameters. (like the Git & Github of Machine Learning)
Folder **Getaround_API** produced an online API that allows using POST method to get the prediction of a Machine Learning model
### Deliverable
- A web dashboard on Heroku (https://getaround-dashboard.herokuapp.com/)
- A Mlflow web on Heroku (https://getaround-mlflow-server.herokuapp.com/)
- An documented online API on Heroku server contains some endpoints including /predict endpoint (https://getaround-api.herokuapp.com/)

