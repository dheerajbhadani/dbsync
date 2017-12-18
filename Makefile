compile-protoc:
	python -m grpc_tools.protoc -I ./protos/. --python_out=./generated/. --grpc_python_out=./generated/. ./protos/db-sync.proto

export PYTHONPATH = ${PWD}
run-server:
	python src/server.py

run-client:
	python src/client.py


