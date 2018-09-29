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

"""The Python gRPC db-sync Server."""

import time
import grpc
import argparse

from generated import db_sync_pb2_grpc, db_sync_pb2
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class DbSyncServicer(db_sync_pb2_grpc.DbSyncServicer):
    """Implements the dbsync API server."""
    def Copy(self, request, conext):
        with open(request.name, "rb") as file_obj:
            while True:
                piece = file_obj.read(request.chunksize)
                if not piece:
                    break
                response = db_sync_pb2.ResponseData()
                response.bytedata = piece
                yield response


def serve(port, shutdown_grace_duration):
    """Configures and runs the dbsync API server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    db_sync_pb2_grpc.add_DbSyncServicer_to_server(DbSyncServicer(), server)
    server.add_insecure_port('[::]:{0}'.format(port))
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(shutdown_grace_duration)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--port', type=int, default=8000, help='The port to listen on')
    parser.add_argument(
        '--shutdown_grace_duration', type=int, default=5,
        help='The shutdown grace duration, in seconds')

    args = parser.parse_args()
    serve(args.port, args.shutdown_grace_duration)
