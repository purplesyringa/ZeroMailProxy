import os
import socket
import sys

from config import zeronet_directory

from smtp.server import Server
from mailbox import Mailbox

server = Server("localhost", 587, Mailbox=Mailbox)
server.serve()