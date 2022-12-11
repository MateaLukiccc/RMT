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
            print(message)
            if message == "Enter 1 for Login and 2 for Registration":
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
                elif next_message == "Please enter required info\nUsername:":
                    username = input("Username: ")
                    client.send(username.encode('ascii'))
                    print(client.recv(1024).decode('ascii'))
                    username = input()
                    client.send(username.encode('ascii'))
                write_thread = threading.Thread(target=write)
                write_thread.start()
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break


def write():
    while True:
        if stop_thread:
            break
        message = f"{username}: {input('')}"
        client.send(message.encode("ascii"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

# write_thread = threading.Thread(target=write)
# write_thread.start()
