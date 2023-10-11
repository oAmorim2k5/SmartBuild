#BANCO DE DADOS
import mysql.connector

email = ""
senha = ""

def conect():
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="smartbd"
    )

    status = connection.ping()

    if connection.is_connected():
        print("O banco de dados está conectado")
    else:
        print("O banco de dados não está conectado")

    return connection