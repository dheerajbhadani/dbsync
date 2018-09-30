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
import argparse_actions
import argparse

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
    def __init__(self, host, port, api_key, auth_token, timeout, chunk_size, source, destination):
        self._source = source
        self._destination = destination
        self._host = host
        self._port = port
        self._chunk_size = chunk_size
        self._api_key = api_key
        self._auth_token = auth_token
        self._timeout = timeout


    def file_data(self, stub):
        source = db_sync_pb2.Source()
        source.name = self._source
        source.chunksize = self._chunk_size

        result = stub.Copy(source, self._timeout)
        response = []
        for data in result:
            response.append(data.bytedata)

        with open(self._destination, "wb") as file_obj:
            file_obj.write("".join(response))


    def copy(self):
        channel = grpc.insecure_channel('{server}:{port}'.format(server=self._host,port=self._port))
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
                           server = self._host,
                           client=socket.gethostbyname(socket.gethostname()),
                           chunk=self._chunk_size))
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
            '--source', metavar='source',
            help='The source file or directory path',
            action='store',
            required=True,
            )
    parser.add_argument(
            '--destination', metavar='destination',
            action='store',
            help='The destination file or directory path',
            required=True,
            )
    parser.add_argument(
            '--host', 
            metavar='host',
            default='localhost',
            action=argparse_actions.ProperIpFormatAction,
            help='The host to connect to',
            )
    parser.add_argument(
            '--port', metavar='port',
            action='store',
            default=8000,
            help='The port to connect to.',
            type=int
            )
    parser.add_argument(
            '--chunk_size', metavar='chunk_size',
            action='store',
            choices=(1024, 2048, 4096, 8192),
            help='Size of each chunk',
            type=int,
            default=8192,
            )
    parser.add_argument(
            '--timeout', 
            type=int, 
            default=30, 
            help='The call timeout, in seconds',
            )
    parser.add_argument(
            '--api_key', 
            default=None, 
            help='The API key to use for the call',
            )
    parser.add_argument(
            '--auth_token', 
            default=None,
            help='The JWT auth token to use for the call',
            )

    try:
            args = parser.parse_args()
            sync_client = DbSyncClient(args.host, args.port, args.api_key, args.auth_token, args.timeout, args.chunk_size, args.source, args.destination)
            sync_client.copy()
    except argparse_actions.NonFolderError as e:
            raise e
