# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The Python gRPC db-sync Client."""

from __future__ import print_function

import time
import grpc

from generated import db_sync_pb2_grpc, db_sync_pb2
import logging
import socket

#SOURCE = "/home/dheerajbhadani/testfiles/output_100M"
SOURCE = "/var/lib/dbsync/test1"

#DESTINATION = "/home/dheerajbhadani/destination/output_100M"
DESTINATION = "/var/lib/test1"
#SERVER = 'localhost'
SERVER = '35.197.246.234'
PORT = 80
CHUNK_SIZE = 8192

_TIMEOUT_SECONDS = 30


"""
#TODO : 
[TimeStamp]|[METHOD]|[SOURCE_LOCATION]|[DESTINATION_LOCATION]|
[Copy Start Time]|[Copy End Time]|[Duration]|[FILESIZE]|[FILETYPE]|
[LATENCY]
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('client.log')
handler.setLevel(logging.INFO)

# create a Logging format
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

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

        logger.info('{source} | {start} | {end} | {time_taken} | '
                    '{server} | {client} | {chunk}'.
                    format(source = self._source,
                           start=start_time,
                           end = end_time,
                           time_taken=diff,
                           server = self._server,
                           client=socket.gethostbyname(socket.gethostname()),
                           chunk=self._chunk_size))
        return True

if __name__ == "__main__":
    sync_client = DbSyncClient(SOURCE, DESTINATION, SERVER, PORT, CHUNK_SIZE)
    sync_client.copy()
