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

TOTAL_TICKETS = 40


def get_remaining_tickets():
    with mydb.cursor() as cursor:
        cursor.execute("SELECT SUM(tickets) FROM reservations")
        OCCUPIED_SEATS = cursor.fetchall()[0][0]
    return TOTAL_TICKETS - OCCUPIED_SEATS


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
users = []


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


def register(username, name, surname, password, jmbg, email, tickets):
    cursor = mydb.cursor(buffered=True)
    try:
        tuple1 = (username, name, surname, password, jmbg, email, tickets)
        cursor.execute(
            'INSERT INTO reservations (username, name, surname, password, jmbg, email, tickets) VALUES (%s, %s, %s, %s, %s, %s, %s)', tuple1)
        mydb.commit()
        print('Logged In!')
        return 1
    except:
        print('Username does not exist')
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
            client.close()
            nickname = users[index]
            broadcast(f"{nickname} left the chat!".encode('ascii'))
            print(f"{nickname} left the chat!")
            users.remove(nickname)
            break


def initial(address, client):
    # while True:
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
                return
                # continue

        elif initial_response == '2':
            client.send("Please enter required info".encode('ascii'))
            client.send("Username: ".encode('ascii'))
            username = client.recv(1024).decode("ascii")

            client.send("Password: ".encode("ascii"))
            password = client.recv(1024).decode("ascii")

            client.send("Name: ".encode("ascii"))
            name = client.recv(1024).decode("ascii")

            client.send("Surname: ".encode("ascii"))
            surname = client.recv(1024).decode("ascii")

            client.send("JMBG: ".encode("ascii"))
            jmbg = client.recv(1024).decode("ascii")
            if len(jmbg) < 13 or len(jmbg) > 13:
                client.send("JMBG too short".encode("ascii"))
                client.close()
                return

            client.send("Email: ".encode("ascii"))
            email = client.recv(1024).decode("ascii")

            client.send("Number of tickets: ".encode("ascii"))
            tickets = client.recv(1024).decode("ascii")
            if int(tickets) < 0 or int(tickets) > get_remaining_tickets():
                client.send("Wrong value for tickets".encode("ascii"))
                client.close()
                return

            result = register(username, name, surname, password, jmbg, email, tickets)
            if result != 1:
                print("ACCESS REFUSED")
                client.send("ACCESS REFUSED".encode("ascii"))
                client.close()
                return

        else:
            print("Please use correct input")
            # continue

        users.append(username)
        clients.append(client)
        print(f"Username of a client is {username}")
        broadcast(f"{username} has joined the chat".encode("ascii"))
        client.send("Connected to the server".encode("ascii"))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()



print("Server is listening...")
while True:
    client, address = server.accept()
    thread = threading.Thread(target=initial, args=(address, client,))
    thread.start()


