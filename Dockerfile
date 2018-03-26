# Pulls base image
FROM python:3.5
# Bundles sources
ADD requirements.txt /tmp/requirements.txt
ADD collection.py /tmp/collection.py
ADD . /git1-collection
WORKDIR /git1-collection
# Setups sources
RUN python3 -m venv ./venv
RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r ./requirements.txt
EXPOSE 5001
CMD ./venv/bin/python ./collection.py