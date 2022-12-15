import socket
import threading

username = ""

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55556))

stop_thread = False


def receive():
    while True:
        #flag = 0
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
                    username = input()
                    client.send(username.encode('ascii'))

                    print(client.recv(1024).decode('ascii'))
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
                    client.send(jmbg.encode('ascii'))

                    print(client.recv(1024).decode('ascii'))
                    email = input()
                    client.send(email.encode('ascii'))

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
    print(client.recv(1024).decode('ascii'))
    print("Please choose to proceed")
    write_thread = threading.Thread(target=write)
    write_thread.start()


# for sending messages while also getting messages
def write():
    print('If you want to exit type any letter')
    while True:
        if stop_thread:
            break
        try:
            while True:
                print(client.recv(1024).decode('ascii'))
                message = input()
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
                    print(client.recv(1024).decode('ascii'))
                    print("You could buy more if there are any tickets left")
        except:
            print("Invalid choice please check your input history for mistakes")
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()





