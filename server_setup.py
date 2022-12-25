import socket

HOST = "127.0.0.1"
PORT = 55556
BUFFER_SIZE = 1024
FORMAT = "ascii"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clients = []
users = []



