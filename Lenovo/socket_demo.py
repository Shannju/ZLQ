import socket
import json
import threading
import numpy as np
from pythonosc import dispatcher
from pythonosc import osc_server
import time
# from sub_data import *

DEBUG_MODE = True

met_rel_values = []
distance = -1
def handle_osc_message(address, *args):
    global met_rel_values
    if address == "/met/eng":
        value = args[0]  # 假设第一个参数是我们需要的值
        print("debug: ", args[0] )
        met_rel_values.append(value)
        # 保持列表长度为5
        if len(met_rel_values) > 3:
            met_rel_values.pop(0)


def check_values_and_send_data(connections):
    global distance
    while True:
        if len(met_rel_values) >= 3:
            # 检查是否所有值都是-1.0
            if all(v == -1.0 for v in met_rel_values):
                if distance != -1:
                    distance = -1
                boolean_value = 0
                float_value = 1
            else:
                boolean_value = 1
                if distance == -1:
                    distance = 1
                x = met_rel_values[-1]
                accelerate = 0.5 - x
                distance += accelerate / 24

                if distance>=1:
                    distance =1
                elif distance <=0:
                    distance=0
                float_value = distance

            data = {
                'boolean_value': boolean_value,
                'float_value': float_value
            }
            json_data = json.dumps(data) + '\\n'  # Append a newline as a delimiter
            print(f"Sent data: {data}")
            # for conn in connections:
            #     conn.sendall(json_data.encode('utf-8'))
            #     print(f"Sent data: {data}")

        time.sleep(1 / 24)  # 每秒发送24帧数据


def setup_osc_server(server_ip, server_port):
    disp = dispatcher.Dispatcher()
    disp.map("/met/rel", handle_osc_message)
    server = osc_server.ThreadingOSCUDPServer((server_ip, server_port), disp)
    print(f"Serving on {server.server_address}")
    server.serve_forever()
# def connect_headset():
#     # Please fill your application clientId and clientSecret before running script
#     your_app_client_id = 't3MbxBkUT3ewiSnfculrMtrSQVctIJrk7koAN8vU'
#     your_app_client_secret = 'X4ZmnfQyuGQMu8FzpTHDb5SBWSpLRFzWdkMnpBvkkX8YPmNyPkJ4CstcXwUto6ZeyS3gsT9LINRChvL0SZZrjMa7KTHlbLfsoxNXdC8FqDIyMzgDLAcmURb3Cf3PD0Kq'
#     s = Subcribe(your_app_client_id, your_app_client_secret)
#
#     # list data streams
#     streams = ['eeg','mot','met','pow']
#     s.start(streams)

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

    data_thread = threading.Thread(target=check_values_and_send_data, args=(connections,))
    data_thread.start()


if __name__ == "__main__":
    main()
