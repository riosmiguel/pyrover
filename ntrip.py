
puerto_com = ''

def inicializar(ser):
    global puerto_com
    puerto_com = ser
    import threading
    threading.Thread(target=go_ntrip, daemon=True).start()


import socket, base64, time, serial, traceback

def go_ntrip():
    global puerto_com
    # basado en https://github.com/MarekGalinski/pyNtrip-simple-client/blob/master/pyNtrip-client.py

    #puerto_com = serial.Serial('/dev/ttyAMA0', 115200, 8, "N", 1, timeout=1)

    server = "rtk.igm.gub.uy"
    port = "2101"
    mountpoint = "UYTA"
    username = "Rtk2025"
    password = "Rtk_2025"

    def getHTTPBasicAuthString(username,password):
        inputstring = username + ':' + password
        pwd_bytes = base64.encodebytes(inputstring.encode("utf-8"))
        pwd = pwd_bytes.decode("utf-8").replace('\n','')
        return pwd

    pwd = getHTTPBasicAuthString(username,password)

    header =\
    "GET /{} HTTP/1.0\r\n".format(mountpoint) +\
    "User-Agent: NTRIP u-blox\r\n" +\
    "Accept: */*\r\n" +\
    "Authorization: Basic {}\r\n".format(pwd) +\
    "Connection: close\r\n\r\n"

    while True:
        cnt = 1
        try:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server,int(port)))

            while True:
                print(cnt)

                s.sendto(header.encode('utf-8'),(server,int(port)))
                resp = s.recv(1024)

                if resp.startswith(b"STREAMTABLE"):
                    print("Invalid or No Mountpoint")
                    exit()
                
                ret = puerto_com.write(resp)
                cnt = cnt + 1
                time.sleep(2)

        except Exception:
            print(traceback.format_exc(-1))
            time.sleep(2)
            
