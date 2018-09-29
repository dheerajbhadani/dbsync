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


def serve():
    """Configures and runs the dbsync API server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    db_sync_pb2_grpc.add_DbSyncServicer_to_server(DbSyncServicer(), server)
    server.add_insecure_port('[::]:40084')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except:
        server.stop(0)

if __name__ == '__main__':
    serve()
