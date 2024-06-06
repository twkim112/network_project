import zmq
import pandas as pd
import time

from tqdm import tqdm

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

df = pd.read_feather(r"B:\Dropbox\Data\BT_Data\stock\min\volume_20240401.arrow")
df = df.fillna(-1)

serialization_times = []
send_times = []
receive_times = []
deserialization_times = []

for attempt in tqdm(range(10)):
    # 직렬화 시간 측정
    start_time = time.time()
    data = df.to_json()
    serialize_time = time.time() - start_time

    # 데이터 전송 시간 측정
    start_time = time.time()
    socket.send_json({'action': 'send', 'data': data})
    socket.recv_string()
    send_time = time.time() - start_time

    # 데이터 수신 시간 측정
    start_time = time.time()
    socket.send_json({'action': 'get'})
    received_data = socket.recv_json()
    receive_time = time.time() - start_time

    # 역직렬화 시간 측정
    start_time = time.time()
    received_df = pd.read_json(received_data)
    deserialize_time = time.time() - start_time

    serialization_times.append(serialize_time)
    send_times.append(send_time)
    receive_times.append(receive_time)
    deserialization_times.append(deserialize_time)

# 결과를 pandas DataFrame으로 변환
results = {
    "attempt": list(range(1, 11)),
    "serialization": serialization_times,
    "deserialization": deserialization_times,
    "sending": send_times,
    "receiving": receive_times
}
df_results = pd.DataFrame(results)
print(df_results)

# CSV 파일로 저장
df_results.to_csv("zeromq_performance_log.csv", index=False)
print("Performance log saved to zeromq_performance_log.csv")
