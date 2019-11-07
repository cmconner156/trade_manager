FROM python:3
MAINTAINER Chris Conner chrism.conner@gmail.com

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
COPY generic-python-flask-supervisord.conf /etc/supervisor/conf.d/generic-python-flask-supervisord.conf

# volumes
VOLUME /application

# workdir ?
WORKDIR /app/

#Install requirements
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

#Environment variables
#ENV PORT 5000
#ENV PYTHONPATH /application
#ENV CWD	/application

#Expose ports
#EXPOSE ${PORT}

#CMD ["/usr/bin/supervisord"]

ENTRYPOINT ["python"]
CMD ["./app.py","--host=0.0.0.0"]
