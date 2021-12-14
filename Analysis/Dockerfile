############################################################
#
# Dockerfile to run a Sentiment Analysis Container
# 
############################################################

# docker build -t masters/sentanalysis:latest .
# docker run -p 5000:5000 masters/sentanalysis:latest


FROM python:3

MAINTAINER swork002@odu.edu

WORKDIR /usr/src/app

RUN pip install flask
RUN pip install nltk
RUN pip install yfinance

COPY ./* ./

EXPOSE 5000

CMD python SentimentAnalysis.py