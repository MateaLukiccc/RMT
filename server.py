import threading
from db import *
from server_setup import *

server.bind((HOST, PORT))
server.listen()


def handle(client, username):
    while True:
        try:
            client.send("Select \n1 for buying tickets \n2 for vip \n3 for remaining tickets \n"
                        "4 to cancel standard tickets \n5 to cancel vip tickets".encode(FORMAT))
            message = client.recv(BUFFER_SIZE).decode(FORMAT)
            if message == '1':
                client.send("How many tickets would u like (0-4)".encode(FORMAT))
                tickets = int(client.recv(BUFFER_SIZE).decode(FORMAT))
                if get_remaining_standard_tickets() < tickets or get_users_tickets(username)+tickets > 4:
                    client.send("You cant buy that many tickets".encode(FORMAT))
                else:
                    buy_tickets(username, tickets)
                    s = f"You have {get_users_tickets(username)} tickets, {get_remaining_standard_tickets()} standard" \
                        f" and {get_remaining_vip_tickets()} vip tickets left"
                    client.send(s.encode(FORMAT))
                    client.send(str(20-get_remaining_standard_tickets()).encode(FORMAT))
            elif message == '2':
                client.send("How many vip tickets would u like (0-4)".encode(FORMAT))
                tickets = int(client.recv(BUFFER_SIZE).decode(FORMAT))
                if get_remaining_vip_tickets() < tickets or get_users_tickets(username) + tickets > 4:
                    client.send("You cant buy that many tickets".encode(FORMAT))
                else:
                    buy_vip_tickets(username, tickets)
                    s = f"You have {get_users_tickets(username)} tickets, {get_remaining_standard_tickets()} standard" \
                        f" and {get_remaining_vip_tickets()} vip tickets left"

                    client.send(s.encode(FORMAT))
                    client.send(str(5 - get_remaining_vip_tickets()).encode(FORMAT))

            elif message == '3':
                client.send("Reservations review:".encode(FORMAT))
                client.send(("You have {} standard and {} vip tickets".format(
                    str(get_users_standard_tickets(username)), str(get_users_vip_tickets(username)))).encode(FORMAT))
                client.send(("There are {} standard tickets and {} vip tickets".format(
                    str(get_remaining_standard_tickets()), str(get_remaining_vip_tickets()))).encode(FORMAT))
            elif message == '4':
                client.send("How many standard tickets would you like to cancel".encode(FORMAT))
                to_cancel = int(client.recv(BUFFER_SIZE).decode(FORMAT))
                if to_cancel > get_users_standard_tickets(username) or to_cancel < 0:
                    client.send("You cant cancel more tickets than you have or less then 0".encode(FORMAT))
                else:
                    cancel_standard_tickets(username, to_cancel)
                    client.send(f"You now have {get_users_standard_tickets(username)} standard tickets".encode(FORMAT))
            elif message == '5':
                client.send("How many vip tickets would you like to cancel".encode(FORMAT))
                to_cancel = int(client.recv(BUFFER_SIZE).decode(FORMAT))
                if to_cancel > get_users_vip_tickets(username) or to_cancel < 0:
                    client.send("You cant cancel more tickets than you have or less then 0".encode(FORMAT))
                else:
                    cancel_vip_tickets(username, to_cancel)
                    client.send(f"You now have {get_users_vip_tickets(username)} vip tickets".encode(FORMAT))

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
    try:

        client.send("Enter 1 for Login and 2 for Registration".encode(FORMAT))
        initial_response = client.recv(BUFFER_SIZE).decode(FORMAT)
        if initial_response == '1':
            client.send("Welcome back".encode(FORMAT))
            client.send("Username: ".encode(FORMAT))
            username = client.recv(BUFFER_SIZE).decode(FORMAT)

            client.send("Password: ".encode(FORMAT))
            password = client.recv(BUFFER_SIZE).decode(FORMAT)
            result = login(username, password)
            if result != 1:
                print("ACCESS REFUSED")
                client.send("ACCESS REFUSED".encode(FORMAT))
                client.close()
                return

        elif initial_response == '2':
            client.send("Please enter required info".encode(FORMAT))
            client.send("Username: ".encode(FORMAT))
            while True:
                username = client.recv(BUFFER_SIZE).decode(FORMAT)

                if check_db_username(username) == 0:
                    client.send("This user already exist\nUsername: ".encode(FORMAT))
                else:
                    break

            client.send("Password: ".encode(FORMAT))
            password = client.recv(BUFFER_SIZE).decode(FORMAT)

            client.send("Name: ".encode(FORMAT))
            name = client.recv(BUFFER_SIZE).decode(FORMAT)

            client.send("Surname: ".encode(FORMAT))
            surname = client.recv(BUFFER_SIZE).decode(FORMAT)

            client.send("JMBG: ".encode(FORMAT))
            jmbg = client.recv(BUFFER_SIZE).decode(FORMAT)
            if len(jmbg) < 13 or len(jmbg) > 13:
                client.send("JMBG too short".encode(FORMAT))
                client.close()
                return

            client.send("Email: ".encode(FORMAT))
            email = client.recv(BUFFER_SIZE).decode(FORMAT)
            client.send("Number of tickets: ".encode(FORMAT))
            tickets = client.recv(BUFFER_SIZE).decode(FORMAT)
            if int(tickets) < 0 or int(tickets) > get_remaining_standard_tickets():
                client.send("Wrong value for tickets".encode(FORMAT))
                client.close()
                return

            result = register(username, name, surname, password, jmbg, email, tickets)
            if result != 1:
                print("ACCESS REFUSED")
                client.send("ACCESS REFUSED".encode(FORMAT))
                client.close()
                return
        else:
            print("Please use correct input")
        users.append(username)
        clients.append(client)
        print(f"Username of a client is {username}")
        client.send(f"{username} has joined the chat".encode(FORMAT))
        client.send("Connected to the server".encode(FORMAT))
        thread1 = threading.Thread(target=handle, args=(client, username,))
        thread1.start()
    except:
        print("Client forcefully closed")


if __name__ == "__main__":
    print("Server is listening...")
    while True:
        cl, addr = server.accept()
        thread = threading.Thread(target=initial, args=(addr, cl,))
        thread.start()
