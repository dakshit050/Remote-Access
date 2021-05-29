import socket
import sys

HEADERSIZE=10
def create_new_socket():
    try:
        global soc
        global port
        global host
        host=""
        port=8080
        soc=socket.socket()
    except socket.error as message:
        print("Socket creation Faild due to : "+str(message))

def socket_binding():
    try:
        global soc
        global port
        global host
        soc.bind((host,port))
        soc.listen(5)
    except socket.error as message:
        print("Socket Binding Faild due to : "+str(message))
        print("Trying Again")
        socket_binding()

def accept_connection():
    try:
        con,address = soc.accept()
        print("Connection established!")
        print("IP "+ address[0]+" Port "+str(address[1]))
        execute_command(con)
        con.close()
    except socket.error as message:
        print("Socket Binding Faild due to : "+str(message))
        

def execute_command(con):
    while True:
        cmd=input()
        if cmd == ":qw":
            print("Connection Lost")
            con.close()
            soc.close()
            sys.exit()
        if len(str.encode(cmd))>0:
            con.send(str.encode(cmd))
            full_msg=''
            new_msg=True
            while True:
                response=con.recv(1024)
                if new_msg:
                    msglen=int(response[:HEADERSIZE])
                    new_msg=False
                full_msg+=response.decode("utf-8")
                if len(full_msg)-HEADERSIZE == msglen:
                    print(full_msg[HEADERSIZE:],end="")
                    new_msg=True
                    full_msg=''
                    break
def main():
    create_new_socket()
    socket_binding()
    accept_connection()

main()   
    
