import os
import socket
import time
import requests
import threading
import subprocess
import sys

# Ensure stdout and stderr are line-buffered. This is crucial for seeing logs in real-time,
# especially when the script runs as a background service.
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# 🖥️ Shutdown the computer
def shutdown_pc():
    """Executes the shutdown command on the system."""
    print("Executing shutdown...")
    os.system("shutdown now")

def show_welcome(video_path="/home/coders/Escritorio/hola.mp4"):
    """
    Opens a video player to show a welcome video on the main display.
    It sets the necessary environment variables (DISPLAY, XAUTHORITY) to interact with the X server.
    """
    print("🎬 Showing welcome video...")

    # Prepare the environment for GUI applications
    env = os.environ.copy()
    env["DISPLAY"] = ":0"

    # If XAUTHORITY is not set, try to find it in a common location for GDM.
    # This is often needed when running the script as a service or from a non-GUI session.
    if "XAUTHORITY" not in env or not os.path.exists(env.get("XAUTHORITY", "")):
        posible_xauth = f"/run/user/{os.getuid()}/gdm/Xauthority"
        if os.path.exists(posible_xauth):
            env["XAUTHORITY"] = posible_xauth

    try:
        # Use Popen to run the command in the background without blocking the agent.
        subprocess.Popen(["xdg-open", video_path], env=env)
        print(f"✅ Video opened: {video_path}")
    except Exception as e:
        print(f"❌ Error opening video: {e}")




def change_wallpaper(image_path="/home/michael/Vídeos/wallpaper.jpg"):
    """Changes the desktop background wallpaper using gsettings."""
    print("🖼️ Changing wallpaper...")
    subprocess.run([
        "gsettings", "set",
        "org.gnome.desktop.background",
        "picture-uri",
        f"file://{image_path}"
    ])


# 🛠️ Check and install snapd if necessary
def ensure_snapd_installed():
    """Checks if snapd is installed and installs it via apt if it's not."""
    try:
        # Check if 'snap' command is available, redirecting output to null
        subprocess.run("snap version", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Snap is already installed.")
    except subprocess.CalledProcessError:
        print("Installing snapd...")
        # Update package list and install snapd
        subprocess.run("sudo apt update -y", shell=True, check=True)
        subprocess.run("sudo apt install snapd -y", shell=True, check=True)

# 💻 Install VSCode without a password (Commented out)
# def install_vscode():
#     """Ensures snapd is present and then installs Visual Studio Code."""
#     ensure_snapd_installed()
#     print("Installing VSCode...")
#     try:
#         subprocess.run("sudo snap install code --classic", shell=True, check=True)
#         print("✅ Installation finished.")
#     except subprocess.CalledProcessError as e:
#         print("❌ Error during installation:", e)

# 🌐 Check local network connection
def is_connected_to_network():
    """
    Checks for local network connectivity by trying to connect to a known local IP.
    Returns True if successful, False otherwise.
    """
    try:
        # Tries to establish a connection to a local server (the manager).
        socket.create_connection(("10.0.120.27", 80), timeout=2)
        return True
    except:
        return False

# 🌍 Check internet connection
def is_connected_to_internet():
    """
    Checks for internet connectivity by trying to connect to Google's DNS server.
    Returns True if successful, False otherwise.
    """
    try:
        # Tries to establish a connection to a reliable external server.
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

# 📡 Report status to the server
def report_status(server_url="http://10.0.120.2:8000/report"):
    """
    Periodically sends the machine's status (hostname, IP, connectivity) to the central server.
    Runs in an infinite loop.
    """
    while True:
        try:
            status_payload = {
                "hostname": socket.gethostname(),
                "ip": socket.gethostbyname(socket.gethostname()),
                "red": is_connected_to_network(),
                "internet": is_connected_to_internet()
            }
            requests.post(server_url, json=status_payload)
            print("Status reported:", status_payload)
        except Exception as e:
            print("Error reporting status:", e)
            # If reporting status fails, try to report the error itself.
            error_payload = {
                "hostname": socket.gethostname(),
                "error": str(e)
            }
            try:
                requests.post("http://10.0.120.2:8000/error", json=error_payload)
            except:
                print("Could not report the error to the server.")
        # Wait for 30 seconds before the next report.
        time.sleep(30)

def update_system():
    """Updates the system packages using apt."""
    print("🔄 Updating system...")
    try:
        subprocess.run("sudo apt update -y", shell=True, check=True)
        subprocess.run("sudo apt upgrade -y", shell=True, check=True)
        print("✅ System updated successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ Error during update:", e)

# 📬 Handle individual connection
def handle_connection(conn, addr):
    """
    Handles a single incoming connection, decodes the command, and executes the corresponding action.
    """
    command = conn.recv(1024).decode().strip()
    print(f"Command received from {addr}: '{command}'")

    if command == "shutdown now":
        shutdown_pc()
    elif command == "apt upgrade":
        update_system()
    elif command == "show welcome":
        # Note: The video path is hardcoded here.
        show_welcome("/home/michael/Vídeos/riwwelcome (1).mp4")
    elif command == "change wallpaper":
        change_wallpaper()
    else:
        print("Command not recognized.")
    conn.close()

# 📡 Listen for commands from the server
def listen_command(port=9876):
    """
    Opens a socket to listen for incoming commands on a specified port.
    Spawns a new thread for each connection.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", port))
    s.listen(5)
    print(f"Agent listening on port {port}...")

    while True:
        conn, addr = s.accept()
        # Start a new daemon thread to handle the connection, allowing for multiple simultaneous commands.
        threading.Thread(target=handle_connection, args=(conn, addr), daemon=True).start()

# 🚀 Start agent
if __name__ == "__main__":
    # Start the status reporting thread in the background.
    threading.Thread(target=report_status, daemon=True).start()
    # Start the main command listening loop.
    listen_command()
