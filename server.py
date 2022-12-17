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

TOTAL_TICKETS = 20
TOTAL_VIP_TICKETS = 5


def get_remaining_standard_tickets():
    with mydb.cursor() as cursor:
        cursor.execute("SELECT SUM(tickets) FROM reservations")
        OCCUPIED_SEATS = cursor.fetchall()[0][0]
    return TOTAL_TICKETS - OCCUPIED_SEATS


def get_users_tickets(username):
    with mydb.cursor() as cursor:
        cursor.execute("SELECT tickets+VipTickets FROM reservations WHERE username=%s", (username,))
        return cursor.fetchone()[0]


def get_users_vip_tickets(username):
    with mydb.cursor() as cursor:
        cursor.execute("SELECT VipTickets FROM reservations WHERE username=%s", (username,))
        return cursor.fetchone()[0]


def get_users_standard_tickets(username):
    with mydb.cursor() as cursor:
        cursor.execute("SELECT tickets FROM reservations WHERE username=%s", (username,))
        return cursor.fetchone()[0]


def buy_tickets(username, tickets):
    with mydb.cursor() as cursor:
        new_tickets=get_users_tickets(username)+tickets
        cursor.execute("UPDATE reservations SET tickets=%s WHERE username=%s", (new_tickets, username,))
        mydb.commit()


def buy_vip_tickets(username, tickets):
    with mydb.cursor() as cursor:
        new_tickets = get_users_vip_tickets(username)+tickets
        cursor.execute("UPDATE reservations SET VipTickets=%s WHERE username=%s", (new_tickets, username,))
        mydb.commit()


def get_remaining_vip_tickets():
    with mydb.cursor() as cursor:
        cursor.execute("SELECT SUM(VipTickets) FROM reservations")
        OCCUPIED_VIP_SEATS = cursor.fetchall()[0][0]
    return TOTAL_VIP_TICKETS-OCCUPIED_VIP_SEATS


def cancel_standard_tickets(username, to_cancel):
    with mydb.cursor() as cursor:
        new_tickets = get_users_tickets(username) - to_cancel
        cursor.execute("UPDATE reservations SET tickets=%s WHERE username=%s", (new_tickets, username,))
        mydb.commit()


def cancel_vip_tickets(username, to_cancel):
    with mydb.cursor() as cursor:
        new_tickets = get_users_vip_tickets(username) - to_cancel
        cursor.execute("UPDATE reservations SET VipTickets=%s WHERE username=%s", (new_tickets, username,))
        mydb.commit()


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


def register(username, name, surname, password, jmbg, email, tickets, VipTickets=0):
    cursor = mydb.cursor(buffered=True)
    try:
        tuple1 = (username, name, surname, password, jmbg, email, tickets, VipTickets)
        cursor.execute(
            'INSERT INTO reservations (username, name, surname, password, jmbg, email, tickets, VipTickets) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', tuple1)
        mydb.commit()
        print('Logged In!')
        return 1
    except:
        print('Username does not exist')
        return 0


def check_db_username(username):
    cursor = mydb.cursor(buffered=True)
    try:
        cursor.execute("SELECT username FROM reservations WHERE username=%s", (username,))
        if cursor.fetchone() is None:
            return 1
        else:
            return 0
    except:
        return 0


def handle(client, username):
    while True:
        try:
            client.send("Select 1 for buying tickets 2 for vip 3 for remaining tickets 4 to cancel standard tickets 5"
                        " to cancel vip tickets".encode('ascii'))
            message = client.recv(1024).decode('ascii')
            if message == '1':
                client.send("How many tickets would u like (0-4)".encode('ascii'))
                tickets = int(client.recv(1024).decode('ascii'))
                if get_remaining_standard_tickets() < tickets or get_users_tickets(username)+tickets > 4:
                    client.send("You cants buy that many tickets".encode('ascii'))
                else:
                    buy_tickets(username, tickets)
                    s = "You have {} tickets, {} standard and {} vip tickets left".format(
                        str(get_users_tickets(username)), str(get_remaining_standard_tickets()),
                        str(get_remaining_vip_tickets()))
                    client.send(s.encode('ascii'))
                    client.send(str(20-get_remaining_standard_tickets()).encode('ascii'))
            elif message == '2':
                client.send("How many vip tickets would u like (0-4)".encode('ascii'))
                tickets = int(client.recv(1024).decode('ascii'))
                if get_remaining_vip_tickets() < tickets or get_users_tickets(username) + tickets > 4:
                    client.send("You cants buy that many tickets".encode('ascii'))
                else:
                    buy_vip_tickets(username, tickets)
                    s = "You have {} tickets, {} standard and {} vip tickets left".format(
                        str(get_users_tickets(username)), str(get_remaining_standard_tickets()),
                        str(get_remaining_vip_tickets()))

                    client.send(s.encode('ascii'))
                    client.send(("There are {} tickets left from which {} are vip tickets".format(
                        str(get_remaining_standard_tickets()), str(get_remaining_vip_tickets()))).encode('ascii'))

            elif message == '3':
                client.send("Reservations review:".encode('ascii'))
                print("Getting users tickets")
                client.send(("You have {} standard and {} vip tickets".format(
                    str(get_users_standard_tickets(username)), str(get_users_vip_tickets(username)))).encode('ascii'))
                client.send(("There are {} standard tickets and {} vip tickets".format(
                    str(get_remaining_standard_tickets()), str(get_remaining_vip_tickets()))).encode('ascii'))
            elif message == '4':
                client.send("How many standard tickets would you like to cancel".encode('ascii'))
                to_cancel = int(client.recv(1024).decode('ascii'))
                if to_cancel > get_users_standard_tickets(username) or to_cancel < 0:
                    client.send("You cant cancel more tickets than you have or less then 0".encode('ascii'))
                else:
                    cancel_standard_tickets(username, to_cancel)
                    client.send(f"You now have {get_users_standard_tickets(username)} standard tickets".encode('ascii'))
            elif message == '5':
                client.send("How many vip tickets would you like to cancel".encode('ascii'))
                to_cancel = int(client.recv(1024).decode('ascii'))
                if to_cancel > get_users_vip_tickets(username) or to_cancel < 0:
                    client.send("You cant cancel more tickets than you have or less then 0".encode('ascii'))
                else:
                    cancel_vip_tickets(username, to_cancel)
                    client.send(f"You now have {get_users_vip_tickets(username)} vip tickets".encode('ascii'))

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = users[index]
            print(f"{nickname} left")
            users.remove(nickname)
            break


def initial(address, client):
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

        elif initial_response == '2':
            client.send("Please enter required info".encode('ascii'))
            client.send("Username: ".encode('ascii'))
            while True:
                username = client.recv(1024).decode("ascii")
                print(username)
                print(check_db_username(username))
                if check_db_username(username) == 0:
                    print('yes')
                    client.send("This user already exist\nUsername: ".encode("ascii"))
                else:
                    break

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
            if int(tickets) < 0 or int(tickets) > get_remaining_standard_tickets():
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

        users.append(username)
        clients.append(client)
        print(f"Username of a client is {username}")
        client.send(f"{username} has joined the chat".encode("ascii"))
        client.send("Connected to the server".encode("ascii"))
        thread = threading.Thread(target=handle, args=(client, username,))
        thread.start()



print("Server is listening...")
while True:
    client, address = server.accept()
    thread = threading.Thread(target=initial, args=(address, client,))
    thread.start()


