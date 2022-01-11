import socket

# THIS SCRIPT IS TO EMULATE THE SIGNAL FROM THE PHONE, IT WILL NOT BE USED IN FINAL RELEASE.

HOST = 'localhost'  # The server's hostname or IP address
PORT = 11417        # The port used by the server

Reg = "MTB203"
Expiry = 60  # Minutes

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    for attempts in range(1, 101):
        try:
            s.connect((HOST, PORT))
            print("[NET] Connection established.")
            s.send(f"{Reg}|{Expiry}".encode('utf-8'))
            print(f"[NET] {Reg}|{Expiry} transmitted, closing connection.")
            s.close()
        except ConnectionRefusedError:
            print(f"[NET] Attempt #{attempts}")
