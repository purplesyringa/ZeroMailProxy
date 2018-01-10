from mailbox import Mailbox
import threading

import pop3.server, smtp.server

def run_server_async(server):
	thread = threading.Thread(target=server.serve)
	thread.start()

run_server_async(pop3.server.Server("localhost", 110, Mailbox=Mailbox))
run_server_async(smtp.server.Server("localhost", 587, Mailbox=Mailbox))