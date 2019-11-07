FROM python:3
MAINTAINER Chris Conner chrism.conner@gmail.com
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

#Install forex stuff
#RUN pip install requests
#RUN pip install paho-mqtt
#RUN pip install flask
#RUN pip install flask_navigation
#RUN pip install psutil
#RUN pip install tablib
#RUN pip install pytz
RUN apt-get update && apt-get install -y supervisor

#Make log dir for supervisor
RUN mkdir -p /var/log/supervisor

#Copy supervisor conf and app
COPY trade-manager-supervisord.conf /etc/supervisor/conf.d/trade-manager-supervisord.conf

# volumes
#VOLUME /application


#Install requirements
WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
#ADD requirements.txt /app/requirements.txt
#RUN pip install -r requirements.txt

#Environment variables
#ENV PORT 5000
#ENV PYTHONPATH /application
#ENV CWD	/application

#Expose ports
#EXPOSE ${PORT}

#CMD ["/usr/bin/supervisord"]

COPY . /

# workdir ?
WORKDIR /app/

ENTRYPOINT ["python"]
CMD ["./app.py","--host=0.0.0.0"]
