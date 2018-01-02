import socket
from util import debug, critical, ServerError
from connection import Connection

class Server(object):
    def __init__(self, host, port, Session):
        self.host = host
        self.port = port
        self.Session = Session
        self.sock = None

    def serve(self):
        if self.sock is not None:
            raise ServerError("Socket already used")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        try:
            debug("Serving")
            while True:
                self.sock.listen(1)
                conn, addr = self.sock.accept()
                try:
                    conn = Connection(conn)
                    session = self.Session(conn)
                finally:
                    conn.close()
        except (SystemExit, KeyboardInterrupt):
            debug("Server quit")
        except Exception as e:
            critical(e)
        finally:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.sock = None