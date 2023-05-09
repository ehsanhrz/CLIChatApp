import socket
import _thread 
import json
from typing import List
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
the first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain
with any two hosts
The second argument is the type of socket. SOCK_STREAM means that data or characters are read in a continuous flow
"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 3:
     print("Correct usage: script, IP address, port number")
     exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.bind((IP_address, Port)) 
#binds the server to an entered IP address and at the specified port number. The client must be aware of these parameters
server.listen(100)
#listens for 100 active connections. This number can be increased as per convenience
list_of_clients=[]

def clientthread(conn, addr,name : str):
    msg = "Welcome to this channel!\n"
    msg = msg.encode()
    conn.send(msg)    
    #sends a message to the client whose user object is conn
    while True:
            try:     
                message = conn.recv(2048)    
                if message:
                    msg = message.decode("utf-8")
                    print(" ["+addr[0]+" ]   "+"<" + name.strip() + "> " + msg)
                    message_to_send = " ["+addr[0]+" ]   "+"<" + name.strip() + "> " + msg
                    broadcast(message_to_send,conn)
                    #prints the message and address of the user who just sent the message on the server terminal
                else:
                    remove(conn)
            except Exception as e:
                print(e,"thread")
                continue

def broadcast(message : str,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                message_to_send = message.encode()
                clients.send(message_to_send)
            except Exception as e:
                print(e , "from Broadcast")
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


        


class user_auth:
    pass

def auth_user(data : List[dict] , user_input_name : str, user_input_password:str ):
    """
    this function takes list of users and searches for the user 
    information, if it  finds it returns true and if not it returns false

    """
    for user in data:
        
        if (user.get("name") == user_input_name.strip()):
            if (user.get("password") == user_input_password.strip()):
                return True

    return False


    

def sign_new_user(new_user : str, new_user_pass : str):
    try:
        with open("users.json","r+") as js:
             
            users : List[dict] = json.load(js)
            
            for i in  users:
                if (i.get("name") == new_user):
                    return False

            users.append({"name":new_user.strip() , "password" : new_user_pass.strip()})
            
            js.seek(0)
            js.truncate()
            
            json.dump(users,js)
            
            return True
    except Exception as e:
        print(e,"asdasdasdasdasd")
        return False

while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """
    msg = "Welcome to this server!\n"
    msg = msg.encode()
    conn.send(msg)

    msg = "enter your user_name\n"
    msg = msg.encode()
    conn.send(msg)
    
    user_input_name : str = conn.recv(2048).decode()

    msg = "enter your password\n"
    msg = msg.encode()
    conn.send(msg)

    user_input_password : str = conn.recv(2048).decode()
    
    
    
    list_of_users  = []

    with open("users.json") as users :
        dummy_data  = json.load(users)
        for i in dummy_data:
            list_of_users.append(i)
    


    result : bool = auth_user(list_of_users,user_input_name,user_input_password)
    


    if(result == True):
        
        
        list_of_clients.append(conn)
        print(addr[0] + " connected")
        #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
        #Prints the address of the person who just connected
        _thread.start_new_thread(clientthread,(conn,addr,user_input_name))
        #creates and individual thread for every user that connects
    else:
        msg = "maybe you enter the name or password wrong or you dont have account\n"
        msg = msg.encode()
        conn.send(msg)

        msg = "you can restart the program or enter 1 to create new user\n"
        msg = msg.encode()
        conn.send(msg)

        user_input = conn.recv(2048).decode()
        if user_input.strip() == "1":
            
            msg = "please enter your name\n"
            msg = msg.encode()
            conn.send(msg)
            
            user_input_name_new = conn.recv(2048).decode()

            msg = "please enter your password\n"
            msg = msg.encode()
            conn.send(msg)
            
            user_input_password_new = conn.recv(2048).decode()

            result_sign : bool = sign_new_user(user_input_name_new,user_input_password)
            if (result_sign):
                list_of_clients.append(conn) 
                print(addr[0]+'connected')
                _thread.start_new_thread(clientthread,(conn,addr,user_input_name_new))

            else:
                msg = "we have this username in database or some bugs happend restart the program and try again\n"
                msg = msg.encode()
                conn.send(msg)
                conn.close()
        
        else:
            conn.close()

