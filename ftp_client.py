import ftplib
import pandas as pd
import time
from io import BytesIO
from tqdm import tqdm

# FTP 서버 접속 정보
FTP_HOST = "127.0.0.1"
FTP_USER = "user"
FTP_PASS = "12345"
FTP_DIR = "/"

# 샘플 데이터
df = pd.read_feather(r"B:\Dropbox\Data\BT_Data\stock\min\volume_20240401.arrow").iloc[:]
df = df.fillna(-1)

serialization_times = []
upload_times = []
download_times = []
deserialization_times = []

for attempt in tqdm(range(10)):
    try:
        # 직렬화 시간 측정
        start_time = time.time()
        data = df.to_csv(index=False).encode('utf-8')  # CSV로 변환 후 바이너리로 인코딩
        serialize_time = time.time() - start_time

        # FTP 업로드 시간 측정
        start_time = time.time()
        with ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
            ftp.cwd(FTP_DIR)
            with BytesIO(data) as f:
                ftp.storbinary(f"STOR dataframe_{attempt}.csv", f)
        upload_time = time.time() - start_time

        # FTP 다운로드 시간 측정
        start_time = time.time()
        with ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
            ftp.cwd(FTP_DIR)
            with BytesIO() as f:
                ftp.retrbinary(f"RETR dataframe_{attempt}.csv", f.write)
                f.seek(0)
                downloaded_data = f.read().decode('utf-8')
        download_time = time.time() - start_time

        # 역직렬화 시간 측정
        start_time = time.time()
        received_df = pd.read_csv(BytesIO(downloaded_data.encode('utf-8')))
        deserialize_time = time.time() - start_time

        serialization_times.append(serialize_time)
        upload_times.append(upload_time)
        download_times.append(download_time)
        deserialization_times.append(deserialize_time)

    except Exception as e:
        print(f"Error during iteration {attempt + 1}: {e}")

# 결과를 pandas DataFrame으로 변환
results = {
    "attempt": list(range(1, 11)),
    "serialization": serialization_times,
    "deserialization": deserialization_times,
    "upload": upload_times,
    "download": download_times
}
df_results = pd.DataFrame(results)
print(df_results)

# CSV 파일로 저장
df_results.to_csv("ftp_performance_log.csv", index=False)
print("Performance log saved to ftp_performance_log.csv")
