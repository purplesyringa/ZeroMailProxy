import os
import socket
import sys

from server import Server
from session import Session

def serve(host, port):
    server = Server(host, port, Session)
    server.serve()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "USAGE: [<host>:]<port>"
    else:
        _, port = sys.argv
        if ":" in port:
            host = port[:port.index(":")]
            port = port[port.index(":") + 1:]
        else:
            host = ""
        try:
            port = int(port)
        except Exception:
            print "Unknown port:", port
        else:
            serve(host, port)