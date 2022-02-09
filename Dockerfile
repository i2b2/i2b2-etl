#Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
#This program and the accompanying materials  are made available under the terms 
#of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
#the terms of the Healthcare Disclaimer.
FROM python:3.10.1-buster


# Creating python virtual environment
RUN python3 -m venv .venv
 
RUN . .venv/bin/activate

RUN python3 -m pip install --upgrade cython

# Installing mssql command line tool
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
 
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
 
RUN apt-get update
RUN apt-get -y install apt-utils
RUN apt-get -y install vim
RUN apt-get install -y postgresql-client smbclient
RUN env ACCEPT_EULA=Y apt-get -y install msodbcsql17
RUN env ACCEPT_EULA=Y apt-get -y install mssql-tools
RUN apt-get -y install unixodbc-dev 
RUN apt-get -y install python-dev graphviz libgraphviz-dev pkg-config 
RUN apt-get -y install python3-sklearn 
RUN apt-get -y install freetds-dev


# Setting env PATH for sqlcmd and bcp
ENV PATH "$PATH:/opt/mssql-tools/bin"

# Installing Docker-client
ENV DOCKERVERSION=19.03.8
RUN curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKERVERSION}.tgz \
  && tar xzvf docker-${DOCKERVERSION}.tgz --strip 1 \
                 -C /usr/bin docker/docker \
  && rm docker-${DOCKERVERSION}.tgz
 
# Installing docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose

# Installing python libraries and modules
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

WORKDIR /usr/src/app
COPY . .

CMD ["/bin/bash"]
