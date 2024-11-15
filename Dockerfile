
# Copyright 2023 Massachusetts General Hospital.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
# Update the package list and install dependencies

RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv 

RUN python3 -m venv .venv
RUN . .venv/bin/activate

RUN apt-get update && apt-get install -y \
    python3-pip \
    curl \
    apt-utils \
    vim \
    postgresql-client \
    unixodbc-dev \
    freetds-dev \
    pkg-config
RUN pip install --upgrade --break-system-packages setuptools
# Create a Python virtual environment and activate it
RUN python3 -m venv /usr/src/app/.venv 
WORKDIR /usr/src/app
RUN . /usr/src/app/.venv/bin/activate
 
# Upgrade pip and install required Python packages
COPY requirements.txt requirements.txt
RUN /usr/src/app/.venv/bin/pip install --upgrade  pip 
RUN /usr/src/app/.venv/bin/pip install --upgrade Cython 
RUN /usr/src/app/.venv/bin/pip install -r requirements.txt 
COPY . .
# Default command
CMD ["/bin/bash"]