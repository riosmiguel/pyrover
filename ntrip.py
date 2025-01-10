import socket
import base64
import time
import serial

#ser = serial.Serial(tty, 19200, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False)
#ser = serial.Serial('/dev/ttyAMA0', 115200, 8, "N", 1, timeout=1)
#ser.flushInput()
#ser.flushOutput()

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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server,int(port)))

while True:
    s.sendto(header.encode('utf-8'),(server,int(port)))
    resp = s.recv(1024)

    if resp.startswith(b"STREAMTABLE"):
        print("Invalid or No Mountpoint")
        exit()
    elif resp.startswith(b"HTTP/1.1 200 OK"):
        print("All good")

    # There are some length bytes at the head here but it actually
    # seems more robust to simply let the higher level RTCMv3 parser do everything
    #length = s.recv(4)
    #try:
    #    length = int(length.strip(), 16)
    #except ValueError:
    #    continue
    
    #data = s.recv(1024)
    print(resp)
       
    #ret = ser.write(data)
    #print(ret)
    #print >>sys.stderr, [ord(d) for d in data]
    #sys.stdout.flush()

    time.sleep(2)