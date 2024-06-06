from zeep import Client
import pandas as pd
import time
from tqdm import tqdm
import numpy as np

client = Client('http://localhost:8000/?wsdl')

df = pd.read_feather(r"B:\Dropbox\Data\BT_Data\stock\min\volume_20240401.arrow")[:40]
df = df.fillna(-1)

serialization_times = []
send_times = []
receive_times = []
deserialization_times = []


# 데이터 프레임을 쪼개는 함수
def split_dataframe(df, chunk_size):
    chunks = []
    num_chunks = len(df) // chunk_size + (1 if len(df) % chunk_size != 0 else 0)
    for i in range(num_chunks):
        chunks.append(df.iloc[i * chunk_size:(i + 1) * chunk_size])
    return chunks


# 데이터 프레임을 20 행 단위로 쪼갬
chunk_size = 20
df_chunks = split_dataframe(df, chunk_size)
total_parts = len(df_chunks)

for attempt in tqdm(range(10)):
    # 직렬화 및 전송 시간 측정
    serialization_time = 0
    sending_time = 0
    for i, chunk in enumerate(df_chunks):
        start_time = time.time()
        data = chunk.to_json(orient='split')
        serialization_time += time.time() - start_time

        start_time = time.time()
        try:
            client.service.send_dataframe_part(data, i, total_parts)
        except Exception as e:
            print(f"Error during send_dataframe_part: {e}")
            continue
        sending_time += time.time() - start_time

    # 데이터 수신 시간 측정
    start_time = time.time()
    try:
        received_data = client.service.get_dataframe()
    except Exception as e:
        print(f"Error during get_dataframe: {e}")
        continue
    receive_time = time.time() - start_time

    # 역직렬화 시간 측정
    start_time = time.time()
    try:
        received_df = pd.read_json(received_data, orient='split')
    except Exception as e:
        print(f"Error during deserialization: {e}")
        continue
    deserialize_time = time.time() - start_time

    serialization_times.append(serialization_time)
    send_times.append(sending_time)
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
df_results.to_csv("soap_performance_log.csv", index=False)
print("Performance log saved to soap_performance_log.csv")
