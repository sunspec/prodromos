import socket
import os
import pypmu

UDP_IP = "10.1.6.21"
UDP_PORT = 5125
sock = socket.socket(socket.AF_INET,  # Internet
                  socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
while True:
    data, addr = sock.recvfrom(4096)  # buffer size is 1024 bytes
    print("received message:", data)