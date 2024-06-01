import socket
import json
import threading
import time

def send_data(conn, float_value):
    while True:
        boolean_value = True  # Actual boolean value
        float_value += 0.01  # Incrementing the floating-point value

        data = {
            'boolean_value': boolean_value,
            'float_value': float_value
        }
        json_data = json.dumps(data) + '\n'  # Append a newline as a delimiter
        conn.sendall(json_data.encode('utf-8'))
        time.sleep(1)  # Send data every second

def receive_data(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        int_value = json.loads(data.decode('utf-8')).get('int_value')
        print(f"Received int_value: {int_value}")

def handle_client(conn):
    float_value = 0.00  # Initialize float_value
    threading.Thread(target=send_data, args=(conn, float_value)).start()
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
