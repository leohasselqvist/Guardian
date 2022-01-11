import socket
import datetime
import time
import threading

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
                    if not data:
                        conn.close()
                        print(f"[HEAD] {addr[0]} disconnected.")
                        break

                    print(f"[HEAD] Received {data} from {addr[0]}")
                    if data == "c":
                        print(f"[HEAD] Camera {addr[0]} verified")
                        cmr_trd = threading.Thread(target=camera, args=(conn, addr))
                        cmr_trd.start()
                        break
                    elif data:
                        park_info = data.split('|')
                        reg = park_info[0]
                        expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=int(park_info[1]))
                        paid_cars[reg] = expiry_time
                        print(f"[PHONE] {addr[0]}: {reg} expiring on {expiry_time}")


def car_checker():
    print("[CHECK] Checker protocol initialized")
    while True:
        chopping_block = []
        for car in parked_cars:
            if car in paid_cars:
                print(f"[CHECK] {car} HAR BETALT")
            else:
                print(f"[CHECK] {car} PARKERAR OLAGLIGT")
        for car in paid_cars:
            if paid_cars[car] < datetime.datetime.now():
                print(f"{car} parkeringstid har gått ut")
                chopping_block.append(car)
        for car in chopping_block:
            paid_cars.pop(car)
        time.sleep(3)


def __main__():
    chckr = threading.Thread(target=car_checker)
    chckr.start()
    networking_head()


if __name__ == "__main__":
    __main__()
