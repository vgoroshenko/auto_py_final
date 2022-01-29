FROM python:3.8-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache git curl unzip openjdk8-jre

RUN mkdir /allure

RUN wget https://github.com/allure-framework/allure2/releases/download/2.17.2/allure-2.17.2.tgz
RUN unzip allure-2.17.2.tgz -d /allure
RUN tar zxvf allure-2.17.2.tgz -C /allure
ENV PATH="/allure/allure-2.17.2/bin:${PATH}"

#ENV CHROME_BIN=/usr/bin/chromium-browser
#RUN export CHROME_BIN=/usr/bin/chromium-browser

WORKDIR /py-app
COPY . .

RUN mkdir /reports
RUN pip3 install -r requirements.txt
RUN pytest -v --tb=line --language=en -m need_review --alluredir=reports

RUN allure generate reports