import socket
import ast
inputQueue = []

def readRequest(payload,client):    
    global inputQueue
    payloadList = payload.split(';')
    for value in payloadList:
        if(value != None):
            valueArray = ast.literal_eval(value)
            valueArray.append(client)
            inputQueue.append(valueArray)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_address = '127.0.0.1'
    server_port = 5000
    server = (server_address,server_port)
    sock.bind(server)
    print "listening to server"
    while True:
        payload, client = sock.recvfrom(4096)    
        readRequest(payload,str(client))
        print inputQueue