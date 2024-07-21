import socket
from threading import Thread
import final_code.price_evaluation as price_evaluation
from final_code.price_evaluation import fetch_prices


def server():
    host = '127.0.0.1'
    port = 12345  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        data = fetch_prices()  
        conn.sendall(str(data).encode())
        conn.close()


if __name__ == '__main__':
    server_thread = Thread(target=server)
    server_thread.start()