FROM ubuntu

RUN apt-get update && apt-get install -y python-pip

# install all the python things
# RUN pip install --upgrade six

# grpc bindings for python
RUN pip install grpcio grpcio-tools

COPY . /app/

WORKDIR /app

EXPOSE 40084
RUN make generate-test-resources
CMD make run-server


