import os
import socket
import time
import requests
import threading
import subprocess
import sys

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# 🖥️ Apagar el equipo
def shutdown_pc():
    print("Ejecutando apagado...")
    os.system("sudo shutdown now")  # ahora no pedirá contraseña

def show_welcome(image_path="/home/coders/Escritorio/mia.jpeg"):
    print("📷 Mostrando imagen de bienvenida...")

    # Copiamos las variables de entorno actuales
    env = os.environ.copy()

    # Forzamos DISPLAY (pantalla gráfica principal)
    env["DISPLAY"] = ":0"

    # Si existe la variable XAUTHORITY, la usamos, si no intentamos con la ruta por defecto
    if "XAUTHORITY" not in env or not os.path.exists(env["XAUTHORITY"]):
        posible_xauth = f"/run/user/{os.getuid()}/gdm/Xauthority"
        if os.path.exists(posible_xauth):
            env["XAUTHORITY"] = posible_xauth

    # Usamos subprocess.Popen para que no bloquee
    try:
        subprocess.Popen(["xdg-open", image_path], env=env)
        print(f"✅ Imagen abierta: {image_path}")
    except Exception as e:
        print(f"❌ Error al abrir la imagen: {e}")
show_welcome()



def change_wallpaper(image_path="/home/michael/Imágenes/wallpaper.jpg"):
    print("🖼️ Cambiando fondo de pantalla...")
    subprocess.run([
        "gsettings", "set",
        "org.gnome.desktop.background",
        "picture-uri",
        f"file://{image_path}"
    ])


# 🛠️ Verificar e instalar snapd si es necesario
def ensure_snapd_installed():
    try:
        subprocess.run("snap version", shell=True, check=True)
        print("Snap ya está instalado.")
    except subprocess.CalledProcessError:
        print("Instalando snapd...")
        subprocess.run("sudo apt update -y", shell=True, check=True)
        subprocess.run("sudo apt install snapd -y", shell=True, check=True)

# 💻 Instalar VSCode sin contraseña
def install_vscode():
    ensure_snapd_installed()
    print("Instalando VSCode...")
    try:
        subprocess.run("sudo snap install code --classic", shell=True, check=True)
        print("✅ Instalación finalizada.")
    except subprocess.CalledProcessError as e:
        print("❌ Error en la instalación:", e)

# 🌐 Verificar conexión a red local
def is_connected_to_network():
    try:
        socket.create_connection(("10.0.120.27", 80), timeout=2)
        return True
    except:
        return False

# 🌍 Verificar conexión a internet
def is_connected_to_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

# 📡 Reportar estado al servidor
def report_status(server_url="http://10.0.120.2:8000/report"):
    while True:
        try:
            estado = {
                "hostname": socket.gethostname(),
                "ip": socket.gethostbyname(socket.gethostname()),
                "red": is_connected_to_network(),
                "internet": is_connected_to_internet()
            }
            requests.post(server_url, json=estado)
            print("Estado reportado:", estado)
        except Exception as e:
            print("Error al reportar estado:", e)
            error_data = {
                "hostname": socket.gethostname(),
                "error": str(e)
            }
            try:
                requests.post("http://10.0.120.2:8000/error", json=error_data)
            except:
                print("No se pudo reportar el error al servidor.")
        time.sleep(30)

def update_system():
    print("🔄 Actualizando sistema...")
    try:
        subprocess.run("sudo apt update -y", shell=True, check=True)
        subprocess.run("sudo apt upgrade -y", shell=True, check=True)
        print("✅ Sistema actualizado correctamente.")
    except subprocess.CalledProcessError as e:
        print("❌ Error durante la actualización:", e)

# 📬 Manejar conexión individual
def handle_connection(conn, addr):
    command = conn.recv(1024).decode().strip()
    print(f"Comando recibido de {addr}: '{command}'")

    if command == "shutdown now":
        shutdown_pc()
    elif command == "apt upgrade":
        update_system()
    elif command == "install vscode":
        install_vscode()
    elif command == "show welcome":
        show_welcome()
    elif command == "change wallpaper":
        change_wallpaper()
    else:
        print("Comando no reconocido.")
    conn.close()

# 📡 Escuchar comandos desde el servidor
def listen_command(port=9876):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", port))
    s.listen(5)
    print(f"Agente escuchando en el puerto {port}...")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_connection, args=(conn, addr), daemon=True).start()

# 🚀 Iniciar agente
if __name__ == "__main__":
    threading.Thread(target=report_status, daemon=True).start()
    listen_command()
