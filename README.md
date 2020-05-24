# mini_DNS_app
A system of three servers that illustrate simplified DNS service.  
Built with Python, Flask, and Docker  

## What does it do?
### Components
__1. User Server (US):__
  - running on port __8080__
  - accepts `GET` HTTP requests at path
    `/fibonacci?hostname={FS_HOSTNAME}&fs_port={FS_PORT}&number={N}&as_ip={AS_IP}&as_port={AS_PORT}`
  - if any parameters are missing, US returns HTTP code `400`, indicating bad request.
  - if request succeed, US returns HTTP code `200` with fibonacci number of sequence number `N`.
  - US need to query AS to learn IP address of `FS_HOSTNAME`.

__2. Fibonacci Server (FS):__
  - running on port __9090__
  - provides Fibonacci number for a given sequence number `N`.
  - 2.1 Registration to AS
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
  - 2.2 Calculate Fibonacci Number  
    - accepts `GET` HTTP request at path `/fibonacci?number={N}`, and returns Fibonacci number for sequence number `N`
    - if it succeed, returns HTTP code `200`.
    - if `N` is not an integer, returns `400` indicating bad format.

__3. Authoritative Server (AS)__
  - accept UDP connection on port __53533__ and register Type A DNS record into database.
  - respond to DNS query on port __53533__. Check the following sample request and response:  
      __request:__  
      ```
      TYPE=A
      NAME=FS_NAME
      ```
      __response:__  
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
  1. User (browser) visit: `http://{SERVER_IP}:{PORT}/fibonacci?hostname={FS_HOSTNAME}&number={N}&as_ip={AS_IP}`
  2. US parses `FS_HOSTNAME` from query string and then query AS for corresponding IP address
  3. AS returns corresponding IP address of `FS_HOSTNAME` to US
  4. US requests `http://{FS_IP}/fibonacci?number={N}`
  5. FS returns answer for the fibonacci number with `200` code
  6. US returns the result to user (browser).

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.  

### Prerequisites
- python, flask
- docker

### Installing
1. clone the project to your local machine 
2. built the image of each server:  
   `docker build -t {user}/{server_name}:latest .`
3. create a Docker network:  
   `docker network create {netwrk_name}`
4. run each container:  
   `docker run --network {netwrk_name} --name {container_name} -p {port}:{port}/udp -it {user}/{server_name}:latest`
   
### Testing
1. learn the IP address of containers:  
   `docker inspect {netwrk_name}`
2. `PUT` a registration request to FS
3. change variables in `test.py` accordingly and run it
