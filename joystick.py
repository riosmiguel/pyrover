import socket, time, traceback

key = ""

def inicializar():
    import threading
    threading.Thread(target=go_joystick, daemon=True).start()

def go_joystick():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 23))
    while True:
        try:
            s.listen()
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            conn.sendall(b"Connected")
            while True:
                data = conn.recv(1024)
                if len(data)>0:
                    str = data.decode("ascii","ignore")
                    if len(str)>0:
                        key = str[-1]
                #conn.sendall(str.encode("ascii"))
                #conn.sendall(b"-")
        
        except Exception:
            print(traceback.format_exc(-1))
            time.sleep(1)

    
