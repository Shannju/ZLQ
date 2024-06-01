# 需求文档

我说一下视频具体的要求

整个视频整体上视角是不变的，只有局部的细节(例如船舶、人物等)有小的移动

而对卷轴整体的移动是在Unity中实现

Unity这边只**从Python脚本接收是否有脑机信号(bool)、船舶距离泉眼的距离(float)两个参数**，只作为显示，不进行任何其他流程的控制。@轰轰烈烈才是爱 在写python脚本时可以注意一下。

没有脑机信号时，卷轴整体水平移动，展示各个朝代的江面。有脑机信号时卷轴停止移动。移动的是卷轴，而不是视频本身，视频本身是不动的。

视频需要左右能拼合上，具体实现方法有两种，从中心全景录制四周环形拼合的河道，或者以正交视图录制直线拼合的河道。

然后我这边Unity里实现的功能是**没有脑机信号**时卷轴横向移动，**有信号**时卷轴停止、泉水和船舶出现在河道中的某处，根据距离实时调整船舶和泉水的距离(同时为了避免过于生硬，方向会进行随机调整)。摘下脑机后船和泉水消失、卷轴继续移动。

![1717250391740](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\1717250391740.png)





```
    import socket
    import json
    import threading
    import time

    def send_data(conn):
        while True:
            boolean_value = False  # 这里可以替换为实际的布尔值
            float_value = 1.0  # 这里可以替换为实际的浮点数值

            data = {
                'boolean_value': boolean_value,
                'float_value': float_value
            }
            conn.sendall(json.dumps(data).encode('utf-8'))
            time.sleep(1)  # 每秒发送一次数据

    def receive_data(conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            int_value = json.loads(data.decode('utf-8')).get('int_value')
            print(f"Received int_value: {int_value}")

    def handle_client(conn):
        threading.Thread(target=send_data, args=(conn,)).start()
        threading.Thread(target=receive_data, args=(conn,)).start()

    def main():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 8765))
        server_socket.listen(1)
        print("Server listening on port 8765")

        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        handle_client(conn)

    if __name__ == "__main__":
        main()


```

