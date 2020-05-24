# mini_DNS_app
A system of three servers that illustrate simplified DNS service.  
Built with Python, Flask, and Docker  

## What dose it do?
### Components
1. User Server (US):
- running on port __8080__
- accepts __GET__ HTTP requestsa at path  
  `/fibonacci?hostname={FS_HOSTNAME}&fs_port={FS_PORT}&number={N}&as_ip={AS_IP}&as_port={AS_PORT}`
- if any parameters are missing, US returns HTTP code `400`, indicating bad request.  
- if request succeed, US returns HTTP code `200` with fibonacci number of sequence number `N`.  
- US need to query AS to learn IP address of `FS_HOSTNAME`.  

2. Fibonacci Server (FS):
- running on port __9090__
- provides Fibonacci number for a given sequence number `N`.

__2.1 Registration to AS__  
- accepts a `PUT` HTTP request at path `/register` where request body contains following JSON object.
```
{
"hostbane": "{FS_HOSTNAME}"
"ip": "{FS_IP}"
"as_ip": "{AS_IP}"
"as_port": "{AS_PORT}"
}
```
- then register it with AS via UDP on port __53533__, using following DNS registration request:  
```
TYPE=A
NAME=FS_NAME
VALUE=FS_IP
TTL=10
```
- if the registration succeed, returns a HTTP response with HTTP code `201`

__2.2 Calculate Fibonacci Number__  
- accepts `GET` HTTP request at path `/fibonacci?number={N}`, and returns Fibonacci number for sequence number `N`
- if it succeed, returns HTTP code `200`.
- if `N` is not an integer, returns `400` indicating bad format.

3. Authoritative Server (AS)
- accept UDP connection on port __53533__ and register Type A DNS record into database.
- respond to DNS query on port __53533__. Check the following sample request and response:  
__request: __  
```
TYPE=A
NAME=FS_NAME
```
__response: __  
```
TYPE=A
NAME=FS_NAME
VALUE=FS_IP
TTL=10
```

### Work Flow
- Preparation:
1. FS registers its hostname with AS
2. AS creates a DNS record for FS and response a result indicating success or failure.

- Main function:
1. User (browser) visit: `http://{server_IP}:{PORT}/fibonacci?hostname={FS_hostname}&number={n}&as_ip={as_IP}`
2. US parses `FS_hostname` from query string and then query AS for corresponding IP address
3. AS returns corresponding IP address of `FS_hostname` to US
4. US requests `http://{FS_IP}/fibonacci?number={n}`
5. FS returns answer for the fibonacci number with 200 code
6. US returns the result to user (browser).

