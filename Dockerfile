FROM python:3.12
ENV TZ="Asia/Kolkata"
RUN date
RUN apk add postgresql-dev
RUN mkdir /home/wikilink
WORKDIR /home/wikilink
COPY requirements.txt .
RUN pip install --upgrade pip setuptools --ignore-installed
RUN pip install -r requirements.txt
CMD flask run --host 0.0.0.0 --port 8080 --debug
EXPOSE 8080

