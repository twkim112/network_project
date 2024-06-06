from flask import Flask, request, jsonify
import pandas as pd
import logging

app = Flask(__name__)
stored_df = None

# 로그 설정
logging.basicConfig(level=logging.DEBUG)


@app.route('/send_dataframe', methods=['POST'])
def send_dataframe():
    global stored_df
    data = request.get_json()
    app.logger.debug(f"Received data: {data[:100]}...")  # 로그에 처음 100자를 출력
    stored_df = pd.read_json(data, orient='split')  # orient='split' 추가
    return jsonify(success=True)


@app.route('/get_dataframe', methods=['GET'])
def get_dataframe():
    global stored_df
    if stored_df is None:
        app.logger.debug("No data available")
        return jsonify(data={})
    app.logger.debug("Sending stored data")
    return stored_df.to_json(orient='split')  # orient='split' 추가


if __name__ == '__main__':
    app.run(debug=True, port=5000)
