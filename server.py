import socket as sk
import threading as td
import pickle as pc
import time
import Database

Database.create_database("chat")

host = "192.168.29.227"     # Enter current IP address
port = 8081

server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
server.bind((host,port))

server.listen()
clients = []
aliases = []
address = []

count = 0

def send(message, source, dest, rec, img):
    time_recieve = time.strftime("%H:%M",time.localtime())
    data = (message,source,time_recieve,img)
    out = pc.dumps(data)
    dest.send(out)
    Database.insert_message(rec, source, 0, message, time_recieve,img, 'chat')

def handle(client):
    global count
    while True:
        try :
            got_from_client = client.recv(10 * 1024 * 1024)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            print("[SERVER] ",alias," ",address[index]," has disconnected from the server [",time.strftime("%H:%M",time.localtime()),"]",sep="")
            count-=1
            print("Active Connections :",count,end="\n\n")
            aliases.pop(index)
            address.pop(index)
            notify_clients(alias)
            break
        got_from_client = pc.loads(got_from_client)
        message = got_from_client[0]
        sender = aliases[clients.index(client)]
        rec = got_from_client[1]
        reciever = ""
        img=got_from_client[3]
        try:
            reciever = clients[aliases.index(rec)]
        except:
            print("[SERVER] ERROR : The reciver of the message was not found")
            print("                ",sender," please recheck your recipient...\n")
            continue
        time_sent = got_from_client[2]
        Database.insert_message(sender, rec, 1, message, time_sent,img, 'chat')
        send(message, sender, reciever, rec, img)

def notify_clients(client_name):
    global clients
    global aliases

    for client_socket in clients:
        try:
            active_users = ', '.join(aliases)
            message = f"{client_name} has joined the chat. Active users: {active_users}"

            data = (message, "SERVER", time.strftime("%H:%M", time.localtime()))
            out = pc.dumps(data)
            client_socket.send(out)

            alias_data = ("ALIAS_LIST", aliases)
            alias_out = pc.dumps(alias_data)
            client_socket.send(alias_out)
        except:
            continue

def connect_client(client, adr):
    global count
    client.send(pc.dumps(("Please send us your name to load data : ",)))
    alias = client.recv(1024).decode()

    # Database Operations and reloading state
    Database.create_user_table(alias, 'chat')
    msg_history = Database.load_data(alias, 'chat')
    if msg_history != 0:
        msg_history = pc.dumps(msg_history)
        client.send(msg_history)

    aliases.append(alias)
    clients.append(client)
    address.append(adr)

    # Notify existing clients about the new client
    notify_clients(alias)

    print("[SERVER] ", alias, " ", adr, " has connected to the server [", time.strftime("%H:%M", time.localtime()), "]", sep="")
    count += 1
    print("Active Connections :", count, end="\n\n")
    thread = td.Thread(target=handle, args=(client,))
    thread.start()

def Server():
    global count
    print("The server is running...\n")
    while True:
        client, adr = server.accept()
        thread1 = td.Thread(target=connect_client, args=(client, adr))
        thread1.start()
        

if __name__ == "__main__":
    Server()
