import threading
from datetime import datetime
from client_setup import *

client.connect((HOST, PORT))
username = ""
stop_thread = False


def receive():
    while True:
        global username
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(BUFFER_SIZE).decode(FORMAT)
            if message == "Enter 1 for Login and 2 for Registration":
                print(message)
                response = input()
                while response.isalpha() or int(response) not in one_two:
                    print("Enter 1 for Login and 2 for Registration")
                    response = input()
                client.send(response.encode(FORMAT))
                next_message = client.recv(BUFFER_SIZE).decode(FORMAT)
                print(next_message)
                if next_message == "Welcome back":
                    print("Please enter required information :)")
                    print(client.recv(BUFFER_SIZE).decode(FORMAT))
                    username = input()
                    client.send(username.encode(FORMAT))
                    print(client.recv(BUFFER_SIZE).decode(FORMAT))
                    password = input()
                    client.send(password.encode(FORMAT))
                    if client.recv(BUFFER_SIZE).decode(FORMAT) == "ACCESS REFUSED":
                        print("Connection was refused! Wrong password!")
                        stop_thread = True
                elif next_message == "Please enter required info":
                    print(client.recv(BUFFER_SIZE).decode(FORMAT))
                    while True:
                        username = input()
                        while len(username) < 2:
                            print("Username must be at least 2 characters long. Please check your input and try again")
                            username = input()
                        client.send(username.encode(FORMAT))
                        message = client.recv(BUFFER_SIZE).decode(FORMAT)
                        print(message)
                        if message == "This user already exist\nUsername: ":
                            continue
                        else:
                            break
                    password = input()
                    while len(password) < 8:
                        print("Password must be at least 8 characters long. Please check your input and try again")
                        password = input()
                    client.send(password.encode(FORMAT))

                    print(client.recv(BUFFER_SIZE).decode(FORMAT))
                    name = input()
                    client.send(name.encode(FORMAT))

                    print(client.recv(BUFFER_SIZE).decode(FORMAT))
                    surname = input()
                    client.send(surname.encode(FORMAT))

                    print(client.recv(BUFFER_SIZE).decode(FORMAT))
                    jmbg = input()
                    while len(jmbg) != 13:
                        print("JMBG must be 13 characters long. Please check your input and try again")
                        jmbg = input()
                    client.send(jmbg.encode(FORMAT))

                    print(client.recv(BUFFER_SIZE).decode(FORMAT))
                    email = input()
                    client.send(email.encode(FORMAT))
                    print(
                        "You can later choose vip tickets if you would like an upgrade this question is just for "
                        "standard tickets")
                    print(client.recv(BUFFER_SIZE).decode(FORMAT))

                    tickets = input()
                    client.send(tickets.encode(FORMAT))
                    if client.recv(BUFFER_SIZE).decode(FORMAT) == "ACCESS REFUSED":
                        print("Connection was refused! Wrong password!")
                        stop_thread = True
                break
            else:
                stop_thread = True
                break
        except:
            print("An error occurred!")
            client.close()
            break
    try:
        print(client.recv(BUFFER_SIZE).decode(FORMAT))
        if not stop_thread:
            print("Please choose to proceed")
        write_thread = threading.Thread(target=write, args=(username,))
        write_thread.start()
    except:
        print("Client closed")


def write(username):
    global stop_thread
    if not stop_thread:
        print('If you want to exit type exit')
    while True:
        if stop_thread:
            break
        try:
            while True:
                print(client.recv(BUFFER_SIZE).decode(FORMAT))
                message = input()
                if message == 'exit':
                    stop_thread = True
                    break

                while message.isalpha() or int(message) not in one_to_five:
                    print("Please choose 1, 2, 3, 4 or 5 if you want to exit type exit")
                    message = input()

                client.send(message.encode(FORMAT))
                received = client.recv(BUFFER_SIZE).decode(FORMAT)
                print(received)
                if received == "How many tickets would u like (0-4)":
                    message = input()
                    while message.isalpha() or int(message) > 4 or int(message) < 0:
                        print("Cant buy more then 4 tickets or fewer then 0\nPlease choose again")
                        message = input()

                    tickets = int(message)
                    client.send(message.encode(FORMAT))
                    m = client.recv(BUFFER_SIZE).decode(FORMAT)
                    print(m)
                    if m != "You cant buy that many tickets":
                        fileTickets = client.recv(BUFFER_SIZE).decode(FORMAT)
                        fileName = username
                        fileDate = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
                        if tickets == 1:
                            with open(f"vip_ticket{fileTickets}.txt", "w") as my_file:
                                my_file.write(f"Congratulations you bought vip ticket number {fileTickets}\n"
                                              f"On username {fileName} at {fileDate}")
                        elif tickets == 2:
                            with open(f"vip_ticket{fileTickets}.txt", "w") as my_file:
                                my_file.write(f"Congratulations you bought vip ticket number {fileTickets} to number "
                                              f"{int(fileTickets) + 1}\n"
                                              f"On username {fileName} at {fileDate}")
                        elif tickets == 3:
                            with open(f"vip_ticket{fileTickets}.txt", "w") as my_file:
                                my_file.write(f"Congratulations you bought vip ticket number {fileTickets} to number "
                                              f"{int(fileTickets) + 2}\n"
                                              f"On username {fileName} at {fileDate}")
                        elif tickets == 4:
                            with open(f"vip_ticket{fileTickets}.txt", "w") as my_file:
                                my_file.write(f"Congratulations you bought vip ticket number {fileTickets} to number "
                                              f"{int(fileTickets) + 3}\n"
                                              f"On username {fileName} at {fileDate}")
                elif received == "How many vip tickets would u like (0-4)":
                    message = input()
                    while message.isalpha() or int(message) > 4 or int(message) < 0:
                        print("Cant buy more then 4 tickets or fewer then 0\nPlease choose again")
                        message = input()

                    tickets = int(message)
                    client.send(message.encode(FORMAT))
                    m = client.recv(BUFFER_SIZE).decode(FORMAT)
                    print(m)
                    if m != "You cant buy that many tickets":
                        fileTickets = client.recv(BUFFER_SIZE).decode(FORMAT)
                        fileName = username
                        fileDate = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
                        if tickets == 1:
                            with open(f"vip_ticket{fileTickets}.txt", "w") as my_file:
                                my_file.write(f"Congratulations you bought vip ticket number {fileTickets}\n"
                                              f"On username {fileName} at {fileDate}")
                        elif tickets == 2:
                            with open(f"vip_ticket{fileTickets}.txt", "w") as my_file:
                                my_file.write(f"Congratulations you bought vip ticket number {fileTickets} to number "
                                              f"{int(fileTickets)+1}\n"
                                              f"On username {fileName} at {fileDate}")
                        elif tickets == 3:
                            with open(f"vip_ticket{fileTickets}.txt", "w") as my_file:
                                my_file.write(f"Congratulations you bought vip ticket number {fileTickets} to number "
                                              f"{int(fileTickets)+2}\n"
                                              f"On username {fileName} at {fileDate}")
                        elif tickets == 4:
                            with open(f"vip_ticket{fileTickets}.txt", "w") as my_file:
                                my_file.write(f"Congratulations you bought vip ticket number {fileTickets} to number "
                                              f"{int(fileTickets)+3}\n"
                                              f"On username {fileName} at {fileDate}")
                elif received == 'Reservations review:':
                    print(client.recv(BUFFER_SIZE).decode(FORMAT))
                    print(client.recv(BUFFER_SIZE).decode(FORMAT))
                elif received == 'How many standard tickets would you like to cancel':
                    to_cancel = input()
                    while to_cancel.isalpha() or int(to_cancel) > 4 or int(to_cancel) < 0:
                        print("Cant cancel more then 4 tickets or fewer then 0\nPlease choose again")
                        to_cancel = input()

                    to_cancel = int(to_cancel)
                    client.send(str(to_cancel).encode(FORMAT))
                    print(client.recv(BUFFER_SIZE).decode(FORMAT))
                elif received == 'How many vip tickets would you like to cancel':
                    to_cancel = input()
                    while to_cancel.isalpha() or int(to_cancel) > 4 or int(to_cancel) < 0:
                        print("Cant cancel more then 4 tickets or fewer then 0\nPlease choose again")
                        to_cancel = input()

                    to_cancel = int(to_cancel)
                    client.send(str(to_cancel).encode(FORMAT))
                    print(client.recv(BUFFER_SIZE).decode(FORMAT))

        except:
            print("Invalid choice please check your input history for mistakes")
            break


if __name__ == "__main__":
    try:
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
    except:
        print("Client closed")
