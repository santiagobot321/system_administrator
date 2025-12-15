import socket
import sys

def send_command(ip, command):
    """
    Sends a command to the agent running on the specified IP.
    Assumes the agent is listening on port 9999.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, 9999))
            s.sendall(command.encode('utf-8'))
            print(f"Command '{command}' sent to {ip}")
    except Exception as e:
        print(f"Error sending command to {ip}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 update_manager.py <ip_address>")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    # The command 'UPDATE' should be recognized by the agent 
    # to trigger the apt update/upgrade process.
    send_command(target_ip, "UPDATE")
