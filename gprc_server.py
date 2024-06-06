import grpc
from concurrent import futures
import sample_df_pb2
import sample_df_pb2_grpc
import pandas as pd
import time

df_message = sample_df_pb2.DataFrame()
stored_df = None


class DataFrameServiceServicer(sample_df_pb2_grpc.DataFrameServiceServicer):
    def GetDataFrame(self, request, context):
        global stored_df
        if stored_df is None:
            return sample_df_pb2.DataFrame()
        return stored_df

    def SendDataFrame(self, request, context):
        global stored_df
        stored_df = request
        return sample_df_pb2.Empty()


def serve():
    # 최대 메시지 크기 설정 (예: 256MB)
    max_message_length = 256 * 1024 * 1024  # 256MB
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_send_message_length', max_message_length),
            ('grpc.max_receive_message_length', max_message_length),
        ]
    )
    sample_df_pb2_grpc.add_DataFrameServiceServicer_to_server(DataFrameServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
