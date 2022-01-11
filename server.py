import socket
import datetime
import time

HOST = 'localhost'  # The server's hostname or IP address
PORT = 11417        # The port used by the server

parked_cars = []
paid_cars = {}


def camera(c, a):
    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            c.close()
            print(f"[CAM] Connection closed by {a[0]}")
            break
        car = data.split('.')  # car[0] is the regplate, car[1] is to add or remove it
        if car[1] == "1":
            parked_cars.append(car[0].upper())
            print(f"[CAM] {car[0]} parked.")
        else:
            try:
                parked_cars.remove(car[0].upper())
                print(f"[CAM] {car[0]} left.")
            except ValueError:
                print(f"[CAM] OVERLOAD I GUESS, VALUE WAS {car[0]}")
        print(f"[CAM] {parked_cars}")


def networking_head():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("[HEAD] Server started.")
        while True:
            print("[HEAD] Listening for client...")
            s.listen(5)  # Now wait for client connection.
            while True:
                conn, addr = s.accept()
                print(f"[HEAD] Client {addr[0]} accepted")
                time.sleep(1)  # Buffer time
                while True:
                    data = conn.recv(1024).decode('utf-8')
                    if data == "c":
                        print(f"[HEAD] Camera {addr[0]} verified")
                        camera(conn, addr)
                        break
                    else:
                        print(f"[PHONE] REG from {addr[0]} ")
                        park_info = data.split('|')
                        reg = park_info[0]
                        expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=int(park_info[1]))
                        paid_cars[reg] = expiry_time
                        print(f"[PHONE] {addr[0]}: {reg} expiring on {expiry_time}")


def __main__():
    networking_head()


if __name__ == "__main__":
    __main__()
