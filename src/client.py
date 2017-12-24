from __future__ import print_function

import time
import grpc

from generated import db_sync_pb2_grpc, db_sync_pb2

#SOURCE = "/home/dheerajbhadani/testfiles/output_100M"
SOURCE = "/var/lib/dbsync/test1"

#DESTINATION = "/home/dheerajbhadani/destination/output_100M"
DESTINATION = "/var/lib/test1"
#SERVER = 'localhost'
SERVER = '35.197.246.234'
PORT = 80
CHUNK_SIZE = 8192

_TIMEOUT_SECONDS = 30


class DbSyncClient(object):
    def __init__(self, source, destination, server, port, chunk_size):
        self._source = source
        self._destination = destination
        self._server = server
        self._port = port
        self._chunk_size = chunk_size


    def file_data(self, stub):
        source = db_sync_pb2.Source()
        source.name = self._source
        source.chunksize = self._chunk_size

        result = stub.Copy(source, _TIMEOUT_SECONDS)
        response = []
        for data in result:
            response.append(data.bytedata)

        with open(self._destination, "wb") as file_obj:
            file_obj.write("".join(response))


    def copy(self):
        channel = grpc.insecure_channel('{server}:{port}'.format(server=self._server,port=self._port))
        stub = db_sync_pb2_grpc.DbSyncStub(channel)
        start_time = time.time()
        self.file_data(stub)
        end_time = time.time()
        diff = end_time - start_time
        print("Start time >> ", start_time, "End time >> ", end_time, "Time taken >> ", diff)

if __name__ == "__main__":
    sync_client = DbSyncClient(SOURCE, DESTINATION, SERVER, PORT, CHUNK_SIZE)
    sync_client.copy()
