from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

# GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) #setup Server

def wait_incoming_connections(SERVER):
    run = True
    while run:
        try:
            client, addr = SERVER.accept()  # wait for any new connections
            person = Person(addr, client)   #Create new person
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            run = False
            break

    print("SERVER CRASHED")

def client_communication(person):
    client = person.client

    #Get Person Name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} has joined you on the chat!", "utf8")
    broadcast(msg, "") # Broadcast Welcome Message

    while True:
        msg = client.recv(BUFSIZ)

        if msg == bytes("{quit}", "utf8"): #if  Quit discomnnect
            client.close()
            persons.remove(person)
            print(f"[Disconnected] {name} Disconnected")
            broadcast(bytes(f"{name} has left the chat...", "utf8"),"")
            break
        else: #Send All the messages to the clients
            broadcast(msg, name+": ")
            print(f"{name}: ", msg.decode("utf8"))
            

def broadcast(msg, name):

    """
    Send new messages to all clients
    param msg: bytes["utf8]
    param name: str
    return:
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name + ":", "utf8") + msg)

        except Exception as e:
            print("[EXCEPTION]", e)
        
    
        

if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  #Open Server for connections
    print("Waiting for Connection")
    ACCEPT_THREAD = Thread(target= wait_incoming_connections, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()