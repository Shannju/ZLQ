import socket
import json
import threading
import numpy as np
from pythonosc import dispatcher
from pythonosc import osc_server
import time
from cortex import Cortex
from sub_data import *

DEBUG_MODE = False

def handle_osc_message(address, *args):
    print(f"Received from {address}: {args}")

def setup_osc_server(server_ip, server_port):
    disp = dispatcher.Dispatcher()
    # 仅处理/met开头的消息
    disp.map("/met*", handle_osc_message)
    server = osc_server.ThreadingOSCUDPServer((server_ip, server_port), disp)
    print(f"Serving on {server.server_address}")
    server.serve_forever()

def send_data(connections, boolean_value, float_value):
    data = {
        'boolean_value': boolean_value,
        'float_value': float_value
    }
    json_data = json.dumps(data) + '\\n'  # Append a newline as a delimiter
    for conn in connections:
        conn.sendall(json_data.encode('utf-8'))
        print(f"Sent data: {data}")

def generate_and_send_data(connections):
    while True:
        boolean_value = True
        # 生成噪声正弦波数据
        float_value = 0.5 + 0.5 * np.sin(time.time()) + np.random.normal(0, 0.05)
        float_value = np.clip(float_value, 0, 1)  # 确保值在0到1之间
        send_data(connections, boolean_value, float_value)
        time.sleep(1 / 24)  # 每秒发送24帧数据

def connect_headset():
    # Please fill your application clientId and clientSecret before running script
    your_app_client_id = 't3MbxBkUT3ewiSnfculrMtrSQVctIJrk7koAN8vU'
    your_app_client_secret = 'X4ZmnfQyuGQMu8FzpTHDb5SBWSpLRFzWdkMnpBvkkX8YPmNyPkJ4CstcXwUto6ZeyS3gsT9LINRChvL0SZZrjMa7KTHlbLfsoxNXdC8FqDIyMzgDLAcmURb3Cf3PD0Kq'
    s = Subcribe(your_app_client_id, your_app_client_secret)

    # list data streams
    streams = ['eeg','mot','met','pow']
    s.start(streams)

def main():
    connections = []
    # Uncomment the following lines if you need to test socket connections as well
    # server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket1.bind(('localhost', 8765))
    # server_socket1.listen(1)
    # print("Socket server listening on port 8765")
    # conn1, addr1 = server_socket1.accept()
    # print(f"Connected by {addr1}")
    # connections.append(conn1)
    #
    # server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket2.bind(('localhost', 8766))
    # server_socket2.listen(1)
    # print("Socket server listening on port 8766")
    # conn2, addr2 = server_socket2.accept()
    # print(f"Connected by {addr2}")
    # connections.append(conn2)

    server_ip = "127.0.0.1"
    server_port = 6868
    osc_thread = threading.Thread(target=setup_osc_server, args=(server_ip, server_port))
    osc_thread.start()

    if DEBUG_MODE:
        # 启动数据生成和发送线程
        data_thread = threading.Thread(target=generate_and_send_data, args=(connections,))
        data_thread.start()

if __name__ == "__main__":
    main()
