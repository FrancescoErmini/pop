FROM python:3.8-slim-buster
RUN apt-get update && apt-get -y install cron vim
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


# run crond as main process of container
CMD ["cron", "-f"]
