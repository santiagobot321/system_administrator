# import socket
# import sys

# def update_system(ip, port=9876):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         s.connect((ip, port))
#         s.sendall(b"apt upgrade")
#         s.close()
#         print(f"Comando de actualización enviado a {ip}:{port}")
#     except ConnectionRefusedError:
#         print("No se pudo conectar al agente.")

# if __name__ == "__main__":
#     pc_ip = sys.argv[1]
#     update_system(pc_ip)
