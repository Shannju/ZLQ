from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client


def process_and_forward_osc_message(address, *args, debug=False):
    # 调试模式下打印原始数据
    if debug:
        print(f"DEBUG - Received from {address}: {args}")

    # 调整数据：将所有数值设置为0.98
    modified_args = [0.98 if isinstance(arg, (int, float)) else arg for arg in args]

    # 发送修改后的数据
    client.send_message(address, modified_args)

    # 调试模式下打印修改后的数据
    if debug:
        print(f"DEBUG - Forwarded to {address}: {modified_args}")


def setup_osc_server(server_ip, server_port, client_ip, client_port, debug=False):
    # 设置分发器
    disp = dispatcher.Dispatcher()
    # 将所有接收到的消息转发到处理函数，并传递调试模式标志
    disp.set_default_handler(lambda addr, *args: process_and_forward_osc_message(addr, *args, debug=debug))

    # 创建OSC服务器实例
    server = osc_server.ThreadingOSCUDPServer((server_ip, server_port), disp)
    print(f"Serving on {server.server_address}")

    # 设置客户端，用于发送数据到另一个端口
    global client
    client = udp_client.SimpleUDPClient(client_ip, client_port)

    # 开始监听
    server.serve_forever()


if __name__ == "__main__":
    # 设置服务器和客户端配置
    server_ip = "127.0.0.1"
    server_port = 6868
    client_ip = "127.0.0.1"
    client_port = 6869

    # 启动服务器
    setup_osc_server(server_ip, server_port, client_ip, client_port, debug=True)
