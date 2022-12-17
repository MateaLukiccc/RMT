import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="online_ticket_reservation"  # to connect to our database
)


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
