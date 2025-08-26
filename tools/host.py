import socket, sys

def send_shutdown(ip, port=9876):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.sendall(b"shutdown now")
    s.close()
    print(f"Shutdown command sent to {ip}:{port}")

if __name__ == "__main__":
    pc_ip = sys.argv[1]
    send_shutdown(pc_ip)
