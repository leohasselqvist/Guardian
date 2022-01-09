import socket


HOST = 'localhost'  # The server's hostname or IP address
PORT = 11417        # The port used by the server

for i in range(0, 100):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            response = ""
            s.connect((HOST, PORT))
            print(f"[NET] Connection made with {HOST}:{PORT}")
            while response != "quit":
                response = input(": ")
                s.sendall(response.encode("utf-8"))
                data = s.recv(1024)
                print('[NET] Received', data.decode("utf-8"))
            else:
                print("[NET] Connection closed")
                break
    except ConnectionRefusedError:
        print(f"[NET] Connection Attempt {i}")
print("[NET] Timed out")
