import requests
import pandas as pd
import time
from tqdm import tqdm
import json
from io import StringIO

# 샘플 데이터
df = pd.read_feather(r"B:\Dropbox\Data\BT_Data\stock\min\volume_20240401.arrow").iloc[:]
df = df.fillna(-1)

serialization_times = []
send_times = []
receive_times = []
deserialization_times = []

for attempt in tqdm(range(10)):
    try:
        # 직렬화 시간 측정
        start_time = time.time()
        data = df.to_json(orient='split')
        serialize_time = time.time() - start_time

        # 데이터 전송 시간 측정
        start_time = time.time()
        response = requests.post('http://localhost:5000/send_dataframe', json=data, timeout=10)
        send_time = time.time() - start_time

        if response.status_code != 200:
            print(f"Error in send_dataframe: {response.status_code}, {response.text}")
            continue

        # 데이터 수신 시간 측정
        start_time = time.time()
        response = requests.get('http://localhost:5000/get_dataframe', timeout=10)
        receive_time = time.time() - start_time

        if response.status_code != 200:
            print(f"Error in get_dataframe: {response.status_code}, {response.text}")
            continue

        # 역직렬화 시간 측정
        start_time = time.time()
        received_data = response.json()
        received_data_str = json.dumps(received_data)  # JSON 데이터를 문자열로 변환
        received_df = pd.read_json(StringIO(received_data_str), orient='split')  # StringIO로 래핑
        deserialize_time = time.time() - start_time

        serialization_times.append(serialize_time)
        send_times.append(send_time)
        receive_times.append(receive_time)
        deserialization_times.append(deserialize_time)

    except requests.exceptions.RequestException as e:
        print(f"Request failed during iteration {attempt + 1}: {e}")
    except ValueError as e:
        print(f"Error during iteration {attempt + 1}: {e}")

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
df_results.to_csv("rest_performance_log.csv", index=False)
print("Performance log saved to rest_performance_log.csv")
