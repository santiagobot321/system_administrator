# tools/install.py
import socket
import sys

def show_welcome(ip, port=9876):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.sendall(b"show welcome")
        print(f"✅ Comando de bienvenida enviado a {ip}:{port}")
    except ConnectionRefusedError:
        print(f"❌ No se pudo conectar al agente en {ip}:{port}. ¿Está corriendo el agente?")
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 install.py <ip_del_pc>")
        sys.exit(1)

    pc_ip = sys.argv[1]
    show_welcome(pc_ip)