compile-protoc:
	python -m grpc_tools.protoc -I ./protos/. --python_out=./generated/. --grpc_python_out=./generated/. ./protos/db-sync.proto

export PYTHONPATH = ${PWD}
run-server:
	python src/server.py

run-client:
	python src/client.py

build-docker:
	docker build -t dbsync:latest .

push-docker:
	docker login
	docker tag my-image username/my-repo
	docker push dheerajbhadani/dbsync
