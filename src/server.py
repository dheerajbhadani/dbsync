import time
import grpc

from generated import db_sync_pb2_grpc, db_sync_pb2
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class DbSyncServicer(db_sync_pb2_grpc.DbSyncServicer):
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
