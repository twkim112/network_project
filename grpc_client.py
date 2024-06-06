import grpc
import sample_df_pb2
import sample_df_pb2_grpc
import pandas as pd
import time
from tqdm import tqdm

df_message = sample_df_pb2.DataFrame()


class CustomPBSerDe:

    def __init__(self, df_message):
        self.message = df_message

    def pbserialise(self, df):
        """ Serialise dataframe to PB. """

        self.message.Clear()  # Ensure the message is clear before starting
        # Set index
        for ts in df.index:
            index = self.message.index.add()
            index.datetime = ts.isoformat()

        # Set columns
        for col in df.columns:
            column = self.message.columns.add()
            column.name = col
            column.values.extend(df[col].astype(float))  # NaN 값을 처리하지 않음

        serialised_data = self.message.SerializeToString()
        return serialised_data

    def pbdeserialise(self, serialised_data):
        """ Deserialise PB message and return dataframe """

        self.message.ParseFromString(serialised_data)

        # Extract index
        idx = [pd.to_datetime(index.datetime) for index in self.message.index]
        idx = pd.DatetimeIndex(idx)

        # Extract columns
        colvalues = {column.name: list(column.values) for column in self.message.columns}

        df = pd.DataFrame(colvalues, index=idx)
        return df


# 클라이언트 코드
def run():
    # 최대 메시지 크기 설정
    max_message_length = 256 * 1024 * 1024  # 256MB
    options = [
        ('grpc.max_send_message_length', max_message_length),
        ('grpc.max_receive_message_length', max_message_length),
    ]
    with grpc.insecure_channel('localhost:50051', options=options) as channel:
        stub = sample_df_pb2_grpc.DataFrameServiceStub(channel)

        # DataFrame 읽기
        df = pd.read_feather(r"B:\Dropbox\Data\BT_Data\stock\min\volume_20240401.arrow")
        df = df.fillna(-1)  # 직렬화 전에 NaN 값을 -1로 대체

        serde = CustomPBSerDe(df_message)

        results = {
            "attempt": [],
            "serialization": [],
            "deserialization": [],
            "sending": [],
            "receiving": []
        }

        for attempt in tqdm(range(10)):
            # 성능 측정: 직렬화
            start_time = time.time()
            serialised_data = serde.pbserialise(df)
            serialize_time = time.time() - start_time

            # DataFrame 직렬화 및 서버로 전송
            df_pb = sample_df_pb2.DataFrame()
            df_pb.ParseFromString(serialised_data)

            # 성능 측정: 데이터 전송
            start_time = time.time()
            stub.SendDataFrame(df_pb)
            send_time = time.time() - start_time

            # 서버로부터 DataFrame 수신
            start_time = time.time()
            received_pb = stub.GetDataFrame(sample_df_pb2.Empty())
            receive_time = time.time() - start_time

            # 성능 측정: 역직렬화
            start_time = time.time()
            deserialised_df = serde.pbdeserialise(received_pb.SerializeToString())
            deserialize_time = time.time() - start_time

            # 결과 저장
            results["attempt"].append(attempt + 1)
            results["serialization"].append(serialize_time)
            results["deserialization"].append(deserialize_time)
            results["sending"].append(send_time)
            results["receiving"].append(receive_time)

        # 결과를 pandas DataFrame으로 변환
        df_results = pd.DataFrame(results)
        print(df_results)

        # CSV 파일로 저장
        df_results.to_csv("grpc_performance_log.csv", index=False)

        print("Performance log saved to performance_log.csv")


if __name__ == '__main__':
    run()
