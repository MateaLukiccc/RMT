import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="online_ticket_reservation"  # to connect to our database
)

# create_db_query = "CREATE DATABASE online_ticket_reservation"
# with mydb.cursor() as cursor:
#     cursor.execute(create_db_query)
#
# show_db_query = "SHOW DATABASES"
# with mydb.cursor() as cursor:
#     cursor.execute(show_db_query)
#     for db in cursor:
#         print(db)

# I want one table that has password username and tickets reserved
create_ticket_table_query = """
CREATE TABLE reservations(
    username VARCHAR(40) PRIMARY KEY ,
    name VARCHAR(40),
    surname VARCHAR(40),
    password VARCHAR(30),
    jmbg VARCHAR(13),
    email VARCHAR(30),
    tickets INT
)   
"""

# with mydb.cursor() as cursor:
#     cursor.execute(create_ticket_table_query)
#     mydb.commit()

show_table_query = "DESCRIBE reservations"
with mydb.cursor() as cursor:
    cursor.execute(show_table_query)
    result = cursor.fetchall()
    for row in result:
        print(row)

# drop_table_query = "DROP TABLE ratings"
# with connection.cursor() as cursor:
#     cursor.execute(drop_table_query)

# adding admin account
insert_reservation_query = """
INSERT INTO reservations (username,name,surname, password,jmbg,email, tickets)
VALUES
    ("ROOT","ROOT","ROOT", "ROOT","1111111111111","admin@admin", 1)
"""
# with mydb.cursor() as cursor:
#      cursor.execute(insert_reservation_query)
#      mydb.commit()

#adding more records
# insert_reviewers_query = """
# INSERT INTO reviewers
# (first_name, last_name)
# VALUES ( %s, %s )
# """
# reviewers_records = [
#     ("Chaitanya", "Baweja"),
#     ("Mary", "Cooper"),
#     ("John", "Wayne"),
#     ("Thomas", "Stoneman"),
#     ("Penny", "Hofstadter"),
#     ("Mitchell", "Marsh"),
#     ("Wyatt", "Skaggs"),
#     ("Andre", "Veiga"),
#     ("Sheldon", "Cooper"),
#     ("Kimbra", "Masters"),
#     ("Kat", "Dennings"),
#     ("Bruce", "Wayne"),
#     ("Domingo", "Cortes"),
#     ("Rajesh", "Koothrappali"),
#     ("Ben", "Glocker"),
#     ("Mahinder", "Dhoni"),
#     ("Akbar", "Khan"),
#     ("Howard", "Wolowitz"),
#     ("Pinkie", "Petit"),
#     ("Gurkaran", "Singh"),
#     ("Amy", "Farah Fowler"),
#     ("Marlon", "Crafford"),
# ]
# with connection.cursor() as cursor:
#     cursor.executemany(insert_reviewers_query, reviewers_records)
#     connection.commit()

# reading records
select_reservations_query = "SELECT * FROM reservations"
with mydb.cursor() as cursor:
    cursor.execute(select_reservations_query)
    result = cursor.fetchall()
    for row in result:
        print(row)

# with where clause
#  select_movies_query = """
# ... SELECT title, collection_in_mil
# ... FROM movies
# ... WHERE collection_in_mil > 300
# ... ORDER BY collection_in_mil DESC
# ... """
# >>> with connection.cursor() as cursor:
# ...     cursor.execute(select_movies_query)
# ...     for movie in cursor.fetchall():
# ...         print(movie)

update_query = """
UPDATE 
    reservations
SET
    tickets = 1
WHERE
    username = "ROOT"
"""
# with connection.cursor() as cursor:
# #     cursor.execute(update_query)
# #     connection.commit()

# delete_query = "DELETE FROM ratings WHERE reviewer_id = 2"
# with connection.cursor() as cursor:
#     cursor.execute(delete_query)
#     connection.commit()


#sum of a column
# cursor = mydb.cursor()
# cursor.execute("SELECT SUM(tickets) FROM reservations")
# print(cursor.fetchall()[0][0])
