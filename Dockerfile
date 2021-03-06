FROM python:3.9.0-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache openjdk8-jre unzip zip chromium chromium-chromedriver

#install allure
RUN mkdir /allure
RUN wget https://github.com/allure-framework/allure2/releases/download/2.17.2/allure-2.17.2.tgz
RUN tar zxvf allure-2.17.2.tgz -C /allure
ENV PATH="/allure/allure-2.17.2/bin:${PATH}"
RUN rm -rf allure-2.17.2.tgz

RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir /reports
RUN pytest -v --tb=line --alluredir=reports -n 3

RUN allure generate reports
RUN cd allure-report/ && zip -r results.zip ./*