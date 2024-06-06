import zmq
import pandas as pd

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

stored_df = None

while True:
    message = socket.recv_json()
    if message['action'] == 'send':
        stored_df = pd.read_json(message['data'])
        socket.send_string("DataFrame received")
    elif message['action'] == 'get':
        if stored_df is None:
            socket.send_json({})
        else:
            socket.send_json(stored_df.to_json())
