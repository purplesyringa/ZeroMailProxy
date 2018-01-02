import os
import socket
import sys

from pop3.server import Server
from mailbox import Mailbox

server = Server("localhost", 110, Mailbox=Mailbox)
server.serve()