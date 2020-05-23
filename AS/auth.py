from socket import *
serverPort = 53533

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
    
print("AS is running...")
while True:
    msg, clientAddr = serverSocket.recvfrom(2048)
    rqstData = msg.decode().split()
    print("Got a request: ", rqstData, len(rqstData))
    if (len(rqstData) == 4):
        try:
            # registration: not handling duplicates
            f = open("DNSdata.txt", "a")
            for i in range(len(rqstData)):
                f.write(rqstData[i])
                if i < len(rqstData) - 1:
                    f.write(", ")
            f.write("\n")
            serverSocket.sendto("Registration Succeeded!".encode(), clientAddr)
        except:
            serverSocket.sendto("Registration Failed!".encode(), clientAddr)        
    elif (len(rqstData) == 2): 
        # respond to DNS Query
        try:
            f = open("DNSdata.txt", "r")
            isFound = 0
            for line in f.readlines():
                DNSdata = line.strip('\n').split(', ')
                if (DNSdata[0] == rqstData[0] and DNSdata[1] == rqstData[1]):
                    isFound = 1
                    break
            if isFound == 0:
                serverSocket.sendto("NOT FOUND!".encode(), clientAddr)
            else:
                rspMsg = ""
                for i in range(len(DNSdata)):
                    rspMsg += DNSdata[i]
                    if i < len(DNSdata) - 1:
                        rspMsg += "\n"
                serverSocket.sendto(rspMsg.encode(), clientAddr)
        except:
            serverSocket.sendto("NOT FOUND!".encode(), clientAddr)
    else:
        serverSocket.sendto("BAD REQUEST!".encode(), clientAddr)
    try:
        f.close()
    except:
        pass
