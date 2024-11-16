# By Ethan Daon
import socket
# used https://docs.python.org/3/library/socket.html for information about the socket library
# also used https://www.geeksforgeeks.org/socket-programming-python/# for a tutorial / examples

def fetch_webpage1():
    # Define the server and the port number
    host = "gaia.cs.umass.edu"
    port = 80

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to the server and create the request
        client_socket.connect((host, port))
        request = "GET /wireshark-labs/INTRO-wireshark-file1.html HTTP/1.1\r\nHost: gaina.cs.umass.edu\r\n\r\n"
        # send the request to the server
        client_socket.sendall(request.encode())

        response = b""
        # receive the response from the server
        while True:
            data = client_socket.recv(1024) # 1024 = # of bytes
            if not data:
                break
            response += data

        print(response.decode())

    finally:
        # close the connection
        client_socket.close()

def fetch_webpage2():
    # Define the server and the port number
    host = "gaia.cs.umass.edu"
    port = 80

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to the server and create the request
        client_socket.connect((host, port))
        request = "GET /wireshark-labs/HTTP-wireshark-file3.html HTTP/1.1\r\nHost:gaia.cs.umass.edu\r\n\r\n"
        # send the request to the server
        client_socket.sendall(request.encode())

        response = b""
        # receive the response from the server
        while True:
            data = client_socket.recv(4096)
            if len(data) <= 0:
                break
            response += data

        print(response.decode())

    finally:
        # close the connection
        client_socket.close()

def start_server():
    # define the server to localhost (127.0.0.1)
    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to the address and port
    server_socket.bind((host, port))

    # start listening for connections
    server_socket.listen(5)
    print(f'Server is listening on {host}:{port}')

    # accept the connection from a clinet
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Recieved connection from {addr}")

        # recieve request from client
        request = client_socket.recv(1024)
        print("Received request:")
        print(request.decode())

        data = "HTTP/1.1 200 OK\r\n" \
               "Content-Type: text/html; charset=UTF-8\r\n\r\n" \
               "<html>Congratulations! You've downloaded the first Wireshark lab file!</html>\r\n"
        
        # send the response to the client
        client_socket.sendall(data.encode())

        # close connection
        client_socket.close()

if __name__ == "__main__":
    # Main function, comment and uncomment functions to run them
    fetch_webpage1()
    fetch_webpage2()
    start_server()
