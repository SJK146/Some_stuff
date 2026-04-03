import socket
import subprocess
import threading

PORT = 8921
target_binary = "./pwnMe"

def handle_client(client_socket):
    try:
       proc = subprocess.Popen(
            ["setarch", "x86_64", "-R", target_binary],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
       payload = client_socket.recv(4096)
       stdout_data, _ = proc.communicate(input=payload)
       client_socket.sendall(stdout_data)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server(port=PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    server.listen(10)

    while True:
        client, addr = server.accept()
        #TODO make this a file logger?
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
