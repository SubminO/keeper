import socket
import os
from stat import S_ISSOCK


class Socket:
    _socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def __init__(self, path):
        self.path = path

    def connect(self):
        with self._socket as s:
            s.connect(self.path)

    def read(self):
        data = self._socket.recv(65535)
        assert data, "Connection closed"
        return data

    def has_socket(self):
        result = True

        try:
            assert os.path.exists(self.path), f"Socket file {self.path} does not exists"
            assert S_ISSOCK(os.stat(self.path).st_mode), f"{self.path} it is not a UNIX socket file"
        except AssertionError as e:
            print(e)
            result = False
        finally:
            return result
