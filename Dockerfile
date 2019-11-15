FROM python:3
MAINTAINER Chris Conner chrism.conner@gmail.com
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
# Install Python and Package Libraries
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim \
    supervisor \
    python3-dev \
    default-libmysqlclient-dev
#    libmariadb-dev-compat \
#    libmariadb-dev \

# Set environment variables
#Python won't try to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
#Makes console output look familiar?
ENV PYTHONUNBUFFERED 1
#SET ENV VAR TO CONFIRM COMMANDS ARE RUN IN THIS CONTAINER
ENV DOCKERCONTAINER=trade_manager

#ENV PORT 5000
#ENV PYTHONPATH /application
#ENV CWD	/application

# volumes
#VOLUME /application

#Expose ports
#EXPOSE ${PORT}


#Install requirements
WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

#Make log dir for supervisor
RUN mkdir -p /var/log/supervisor

#Copy supervisor conf and app
COPY trade-manager-supervisord.conf /etc/supervisor/conf.d/trade-manager-supervisord.conf

#Add wait-for-it for dependency check
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Project Files and Settings
ARG PROJECT=trade_manager
ARG PROJECT_DIR=/app/
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
#ADD . $PROJECT_DIR

# Server
EXPOSE 8000
STOPSIGNAL SIGINT
#ENTRYPOINT ["python", "manage.py"]
#CMD ["runserver", "0.0.0.0:8000"]