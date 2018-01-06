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
run-tests:
	coverage run --source=. -m unittest discover -s tests/
show-test-coverage:
	coverage report -m

generate-test-resources:
	dd if=/dev/zero of=${PWD}/test_10m count=10 bs=1M
	dd if=/dev/zero of=${PWD}/test_100m count=100 bs=1M
	dd if=/dev/zero of=${PWD}/test_250m count=250 bs=1M
