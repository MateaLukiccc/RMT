import socket
import threading

username = ""

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55556))

stop_thread = False


def receive():
    while True:
        global username
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode("ascii")
            # print(message)
            if message == "Enter 1 for Login and 2 for Registration":
                print("Enter 1 for Login and 2 for Registration")
                response = input()
                client.send(response.encode("ascii"))
                next_message = client.recv(1024).decode('ascii')
                print(next_message)
                if next_message == "Welcome back":
                    print("Please enter required information :)")
                    print(client.recv(1024).decode('ascii'))
                    username = input()
                    client.send(username.encode('ascii'))
                    print(client.recv(1024).decode('ascii'))
                    password = input()
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == "ACCESS REFUSED":
                        print("Connection was refused! Wrong password!")
                        stop_thread = True
                elif next_message == "Please enter required info":
                    print(client.recv(1024).decode('ascii'))
                    while True:
                        username = input()
                        while len(username) < 2:
                            print("Username must be at least 2 characters long. Please check your input and try again")
                            username = input()
                        client.send(username.encode('ascii'))
                        message = client.recv(1024).decode('ascii')
                        print(message)
                        if message == "This user already exist\nUsername: ":
                            continue
                        else:
                            break
                    password = input()
                    while len(password) < 8:
                        print("Password must be at least 8 characters long. Please check your input and try again")
                        password = input()
                    client.send(password.encode('ascii'))

                    print(client.recv(1024).decode('ascii'))
                    name = input()
                    client.send(name.encode('ascii'))

                    print(client.recv(1024).decode('ascii'))
                    surname = input()
                    client.send(surname.encode('ascii'))

                    print(client.recv(1024).decode('ascii'))
                    jmbg = input()
                    while len(jmbg) != 13:
                        print("JMBG must be 13 characters long. Please check your input and try again")
                        jmbg = input()
                    client.send(jmbg.encode('ascii'))

                    print(client.recv(1024).decode('ascii'))
                    email = input()
                    client.send(email.encode('ascii'))
                    print(
                        "You can later choose vip tickets if you would like an upgrade this question is just for "
                        "standard tickets")
                    print(client.recv(1024).decode('ascii'))

                    tickets = input()
                    client.send(tickets.encode('ascii'))
                    if client.recv(1024).decode('ascii') == "ACCESS REFUSED":
                        print("Connection was refused! Wrong password!")
                        stop_thread = True
                break
            else:
                stop_thread = True
                break
            print(client.recv(1024).decode('ascii'))
        except:
            print("An error occurred!")
            client.close()
            break
    try:
        print(client.recv(1024).decode('ascii'))
        if not stop_thread:
            print("Please choose to proceed")
        write_thread = threading.Thread(target=write)
        write_thread.start()
    except:
        print("Client closed")


def write():
    global stop_thread
    if not stop_thread:
        print('If you want to exit type exit')
    while True:
        if stop_thread:
            break
        try:
            while True:
                print(client.recv(1024).decode('ascii'))
                message = input()
                if message == 'exit':
                    stop_thread = True
                    break
                elif message != '1' and message != '2' and message != '3':
                    print("Please choose 1 2 or 3 if you want to exit type exit")

                client.send(message.encode("ascii"))
                received = client.recv(1024).decode('ascii')
                print(received)
                if received == "How many tickets would u like (0-4)":
                    message = input()
                    tickets = int(message)
                    while tickets > 4 or tickets < 0:
                        print("Cant buy more then 4 tickets or fewer then 0\nPlease choose again")
                        message = input()
                        tickets = int(message)
                    client.send(message.encode("ascii"))
                    print(client.recv(1024).decode('ascii'))
                    print("Thank you for choosing our company")
                    print("You could buy more if there are any tickets left")
                elif received == "How many vip tickets would u like (0-4)":
                    message = input()
                    tickets = int(message)
                    while tickets > 4 or tickets < 0:
                        print("Cant buy more then 4 tickets or fewer then 0\nPlease choose again")
                        message = input()
                        tickets = int(message)
                    client.send(message.encode("ascii"))
                    print(client.recv(1024).decode('ascii'))
                    print("Thank you for choosing our company")
                    print("You could buy more if there are any tickets left")
                elif received == 'Reservations review:':
                    print(client.recv(1024).decode('ascii'))
                    print("Thank you for choosing our company")


        except:
            print("Invalid choice please check your input history for mistakes")
            break


if __name__ == "__main__":
    try:
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
    except:
        print("Client closed")





