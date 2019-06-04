#!/usr/bin/env python
# coding: utf-8



import socket


HOST = '10.46.220.195'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    while True:
        wel = input()
        conn.send(bytes(wel, "utf-8"))
        data = conn.recv(1024)
        print(data.decode("utf-8"))
        if wel == "bye":
            break

 




