import socket
import threading
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="online_ticket_reservation"  # to connect to our database
)

host = "127.0.0.1"
port = 55556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def login(username, password):
    cursor = mydb.cursor(buffered=True)
    try:
        tuple1 = (username, password)
        cursor.execute(
            'SELECT username FROM reservations WHERE username = %s AND password = %s', tuple1)
        result = cursor.fetchone()
        if result is None:
            return 0
        print('Logged In!')
        return 1
    except:
        print('Username is not exist')
        return 0


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode('ascii'))
            nicknames.remove(nickname)
            break


def initial():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("Enter 1 for Login and 2 for Registration".encode("ascii"))
        initial_response = client.recv(1024).decode("ascii")

        if initial_response == '1':
            client.send("Welcome back".encode('ascii'))
            client.send("Username: ".encode('ascii'))
            username = client.recv(1024).decode("ascii")

            client.send("Password: ".encode("ascii"))
            password = client.recv(1024).decode("ascii")
            result = login(username, password)
            if result != 1:
                print("ACCESS REFUSED")
                client.send("ACCESS REFUSED".encode("ascii"))
                client.close()
                continue

        elif initial_response == '2':
            client.send("Please enter required info\nUsername:".encode('ascii'))
            username = client.recv(1024).decode("ascii")

            client.send("Password: ".encode("ascii"))
            password = client.recv(1024).decode("ascii")

            cursor = mydb.cursor(buffered=True)

            checkUsername = cursor.execute(
                f'INSERT INTO reservations (username, password, tickets) VALUES ({username}, {password}, 0)')
        else:
            print("Please use correct input")
            continue

        print(f"Username of a client is {username}")
        broadcast(f"{username} has joined the chat".encode("ascii"))
        client.send("Connected to the server".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
initial()
