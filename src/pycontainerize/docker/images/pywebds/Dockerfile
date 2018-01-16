# Copyright 2013 Thatcher Peskens, Anshuman Kanetkar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# hacksummit2016

# from debian:stable
from ubuntu:trusty

maintainer tooringanalytics

# Set up the repositories
# run echo "deb http://httpredir.debian.org/debian stable main non-free contrib" > /etc/apt/sources.list && \
#     echo "deb-src http://httpredir.debian.org/debian stable main non-free contrib" >> /etc/apt/sources.list && \
#     echo "deb http://security.debian.org stable/updates main non-free contrib" >> /etc/apt/sources.list && \
#     echo "deb-src http://security.debian.org stable/updates main non-free contrib" >> /etc/apt/sources.list

# Install the base image
run apt-get update
run apt-get install -y build-essential git
run apt-get install -y python python-dev python-setuptools
run apt-get install -y wget nano locales curl unzip wget openssl libhdf5-dev
run apt-get install -y supervisor
run easy_install pip
run pip install --upgrade pip

# install uwsgi now because it takes a little while
run pip install uwsgi

# install python dependencies
run apt-get install -y python-software-properties

# Install database clients
run apt-get install -y sqlite3
run apt-get install -y postgresql-client libpq-dev

# Install Python PILlow dependencies
run apt-get install -y libffi-dev libtiff5-dev libjpeg-turbo8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev

# Install memcache dependencies
run apt-get install -y libsasl2-2


# Install and setup minimal Anaconda Python distribution
# RUN wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
# RUN bash miniconda.sh -b -p /anaconda && rm miniconda.sh
# ENV PATH /anaconda/bin:$PATH

# Install some essential data science packages in python, including psycopg2
# RUN conda install scipy numpy scikit-learn scikit-image pyzmq nose readline pandas matplotlib seaborn dateutil ipython-notebook nltk pip
# RUN conda install psycopg2
# RUN conda install cython hdf5 pytables
#
# # Get plotly
# RUN pip install plotly
#
# # Get the latest gensim
# RUN pip install gensim
#
# # get all the nltk data
# # RUN python -m nltk.downloader all

RUN apt-get build-dep -y python-numpy python-scipy python-matplotlib python-pandas scikit-learn ipython ipython-notebook python-sympy python-nose

# Install Node.js & bower
# Install Node.js
RUN \
  cd /tmp && \
  curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash - && \
  sudo apt-get update && \
  sudo apt-get install -y nodejs && \
  npm install -g npm && \
  printf '\n# Node.js\nexport PATH="node_modules/.bin:$PATH"' >> /root/.bashrc
RUN npm install -g bower
RUN npm install -g gulp-cli
RUN echo '{ "allow_root": true }' > /root/.bowerrc

# RUN \
#   cd /tmp && \
#   wget http://nodejs.org/dist/node-latest.tar.gz && \
#   tar xvzf node-latest.tar.gz && \
#   rm -f node-latest.tar.gz && \
#   cd node-v* && \
#   ./configure && \
#   CXX="g++ -Wno-unused-local-typedefs" make && \
#   CXX="g++ -Wno-unused-local-typedefs" make install && \
#   cd /tmp && \
#   rm -rf /tmp/node-v* && \
#   npm install -g npm && \
#   printf '\n# Node.js\nexport PATH="node_modules/.bin:$PATH"' >> /root/.bashrc
# RUN npm install -g bower
# RUN echo '{ "allow_root": true }' > /root/.bowerrc

RUN apt-get install -y mongodb-clients

EXPOSE 443 80

ADD ./entrypoint.sh /home/docker/

# Mutable volumes for application code & server logs.
VOLUME /home/docker/code
VOLUME /home/docker/logs

# $ docker run -d -P --name webdocker -v /home/docker/config:/opt/tooring/config tooringanalytics/pywebds

ENTRYPOINT ["/home/docker/entrypoint.sh"]
