import socket
import requests
import random,time

server_address = '127.0.0.1'
server_port = 5000

def nameGenerator():
    name_generator = "http://namey.muffinlabs.com/name.json?count=1&with_surname=true&frequency=all"    
    response = requests.get(name_generator)
    return str(response.json()[0])

def createRequest(msg_id):
    payload = [msg_id,nameGenerator(),random.randint(0,3)]    
    return str(payload)

def sendReqest(socket,message):
    print("Msg to be sent: " + message)
    socket.sendto(message, (server_address, server_port))

if __name__ == '__main__':
    msg_id = 0
    payload = ""
    udpClient_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + 3
    while time.time() < end_time:
        msg_id += 1
        payload = payload + (createRequest(msg_id) + ";")
    sendReqest( udpClient_Socket, payload[:-1])

