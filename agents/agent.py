import os
import socket

"Create a function that shutdown a PC"

def shutdown_pc ():

    """shutdown local PC"""
    os.system("shutdown now")


"Create another function that listen for commands"

def listen_command(port=9876):

    """Listening commands from server"""

    "socket.socket create a socket, AF_INET it's IPv4 and SOCK_STREAM it's TCP"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    "bind is used to hook a specific IP and port."
    s.bind(("", port))
    "listen converts socket into a server and 1 is the maximun number of connections allowed."
    s.listen(1)
    print(f"Agent listening on port {port}...")

    while True:

        "Script waiting for conections"
        conn, addr = s.accept()

        "command is received in bytes and then translated into string"
        command = conn.recv(1024).decode()
        if command == "shutdown now":
            print(f"Received shutdown command from {addr}")
            shutdown_pc()
        conn.close()


if __name__ == "__main__":
    listen_command()