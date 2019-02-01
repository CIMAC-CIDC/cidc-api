FROM python:3.6

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
RUN pip3 uninstall bson --yes
RUN pip3 uninstall pymongo --yes
RUN pip3 install pymongo --user
COPY . /app
WORKDIR /app
