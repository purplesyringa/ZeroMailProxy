import os
import socket
import sys

from pop3.server import Server
from pop3.mailbox import Mailbox

server = Server("localhost", 110, Mailbox=Mailbox)
server.serve()