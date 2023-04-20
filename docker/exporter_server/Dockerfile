FROM python:3.11

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD static/ /server/static/

ADD exporter_server.py /server/
ADD scraper_tm_intervals.py /server/

EXPOSE 9090

WORKDIR /server/
