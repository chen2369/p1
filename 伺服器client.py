import socket

HOST = '10.46.220.195'  # The server's hostname or IP address
PORT = 65432            # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
#    data = s.recv(1024)
#    print(data.decode("utf-8"))
    while True:
        data1 = s.recv(1024)
        print(data1.decode("utf-8"))
        if data1.decode("utf-8") == "bye":
            break
        hello = input()
        s.send(bytes(hello, "utf-8"))