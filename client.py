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
                    username = input()
                    client.send(username.encode('ascii'))
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
            else:
                print(message)
            write_thread = threading.Thread(target=write)
            write_thread.start()
        except:
            print("An error occurred!")
            client.close()
            break


# for sending messages while also getting messages
def write():
    while True:
        if stop_thread:
            break
        try:

            message = f"{username}: {input('')}"
            client.send(message.encode("ascii"))
        except:
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()


