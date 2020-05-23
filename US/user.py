from flask import Flask, request, abort
from socket import *
import requests

hostIP = "0.0.0.0"
serverPort = 8080
app = Flask(__name__)
#app.debug = True

@app.route("/")
def hello():
    return "<h1>Hello, This is the User Server</h1>"

@app.route("/fibonacci/", methods=['GET'])
def getFibnum():
    hostname = request.args.get("hostname") 
    fs_port = request.args.get("fs_port")     
    number = request.args.get("number")     
    as_ip = request.args.get("as_ip")     
    as_port = request.args.get("as_port")   
    if (hostname == None or fs_port == None or number == None or as_ip == None or as_port== None):
        abort(400)
    fs_ip = queryFSIP(hostname, as_ip, as_port)
    url = "http://{}:{}/fibonacci?number={}".format(fs_ip, fs_port, number)
    answer = requests.get(url, timeout=2.50).text
    return answer, 200

def queryFSIP(hostname, as_ip, as_port):
    UDP_socket = socket(AF_INET, SOCK_DGRAM)
    msg = "TYPE=A\nNAME={}\n".format(hostname)
    UDP_socket.sendto(msg.encode(), (as_ip, int(as_port)))
    fs_ip = None
    while fs_ip == None:
        recvMsg, serverAddr = UDP_socket.recvfrom(2048)
        fs_ip = recvMsg.decode().split()[2].split('=')[1]
#        print("Receiving fs_ip: ", fs_ip)
    UDP_socket.close()
    return fs_ip

if __name__ == "__main__":
    app.run(host=hostIP, port=serverPort)
