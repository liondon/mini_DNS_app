from flask import Flask, request, abort
from socket import *
import time
hostIP = "0.0.0.0"
serverPort = 9090

app = Flask(__name__)
#app.debug = True

@app.route("/")
def hello():
    return "<h1>Hello, This is the Fibonacci Server</h1>"

@app.route("/register/", methods=['PUT'])
def register():
    requestData = request.get_json()
    data = { 
        'hostname': requestData['hostname'], 
        'ip': requestData['ip'], 
        'as_ip': requestData['as_ip'], 
        'as_port': requestData['as_port'] 
    } 
    if (data['hostname'] == None or data['ip'] == None or data['as_ip'] == None or data['as_port'] == None):
        abort(400)

    # Registration to Authoritative Server
    Socket_UDP = socket(AF_INET, SOCK_DGRAM)
    DNSMsg = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10\n".format(data['hostname'], data['ip'])
    try:
        Socket_UDP.sendto(DNSMsg.encode(), (data['as_ip'], int(data['as_port'])))
    except:
        ## indicating cannot send UDP msg to AS
        abort(503)  

    recvMsg = None
    timeout = 300
    Start = time.time()
    while recvMsg == None and time.time() < Start + timeout:
        recvMsg, serverAddr = Socket_UDP.recvfrom(2048)
        recvMsg = recvMsg.decode()
    if recvMsg == "Registration Succeeded!":
        return '', 201
    elif recvMsg == None:
        return "TIMEOUT: No response from AS!"
    else:
        return recvMsg
    Socket_UDP.close()

@app.route("/fibonacci/", methods = ['GET'])
def fibonacci():
    try:
        print("Got a request: ", request.args.get("number"))
        n = int(request.args.get("number"))
    except:
        abort(400)
    return str(fib(n)), 200

def fib(n):
    minusTwo = 0
    minusOne = 1
    for i in range(2, n + 1):
        answer = minusOne + minusTwo
        minusTwo = minusOne
        minusOne = answer
    return answer
    
if __name__ == "__main__":
    app.run(host=hostIP, port=serverPort)
