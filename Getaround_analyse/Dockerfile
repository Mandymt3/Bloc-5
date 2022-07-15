FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update


RUN pip install pandas streamlit plotly openpyxl
COPY . /home/app

CMD streamlit run --server.port $PORT streamlit_app.py