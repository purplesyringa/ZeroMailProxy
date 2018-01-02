import socket, traceback, threading
from util import debug, critical, ServerError
from connection import Connection
from session import Session

class Server(object):
    def __init__(self, host, port, Mailbox):
        self.host = host
        self.port = port
        self.Mailbox = Mailbox
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

                thread = threading.Thread(target=self.run, args=(conn,))
                thread.daemon = True
                thread.start()
        except (SystemExit, KeyboardInterrupt):
            debug("Server quit")
        except Exception as e:
            critical(traceback.format_exc())
        finally:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.sock = None

    def run(self, conn):
        try:
            conn = Connection(conn)
            session = Session(conn, Mailbox=self.Mailbox)
        finally:
            conn.close()