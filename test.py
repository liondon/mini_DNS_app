import requests
from flask import jsonify
US_hostname = "127.0.0.1"
US_port = 8080
FS_ip = "127.0.0.1"
FS_hostname = "fibonacci.com"
FS_port = 9090
number = 10
AS_ip = "127.0.0.1"
AS_port = "53533"

## US: correct request: response the fibonacci number
url = "http://{}:{}/fibonacci?hostname={}&fs_port={}&number={}&as_ip={}&as_port={}".format(US_hostname, US_port, FS_hostname, FS_port, number, AS_ip, AS_port)
response = requests.get(url, timeout=2.50)
print(response.status_code, response.text)

## US: bad request: response 404
url = "http://{}:{}/fibonacci?hostname={}&fs_port={}&number={}&as_ip={}".format(US_hostname, US_port, FS_hostname, FS_port, number, AS_ip, AS_port)
response = requests.get(url, timeout=2.50)
print(response.status_code, response.text)


## FS: PUT registration, errors cannot solve, use postman instead!
while False:
    data = { 
        "hostname": "fibonacci.com", 
        "ip": "172.18.0.2", 
        "as_ip": "127.0.0.1", 
        "as_port": "53533" 
    } 
    r = requests.put("https://{}:{}/register/".format(FS_ip, FS_port), jsonify(data))
    
    
print("Press Enter to end the process.")
input()
    