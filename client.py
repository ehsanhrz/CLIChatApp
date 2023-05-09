import socket
import select
import sys
import msvcrt
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

while True:
    sockets_list = [server]
    read_sockets = select.select(sockets_list, [], [], 1)[0]
        
    if msvcrt.kbhit(): read_sockets.append(sys.stdin)
    # read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            message = message.decode('utf-8')
            print (message)
        else:
            message = sys.stdin.readline()
            msg = message.encode()
            server.send(msg)
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()
