import os
import telebot
import mysql.connector
from mysql.connector import Error

connected=False
fname=""

def write_table(qr):
    try:
        connection = mysql.connector.connect(host='localhost',database='Users',user='root',password='root')

        if connection.is_connected():
            db_info = connection.get_server_info()
            cursor = connection.cursor(buffered=True)
            cursor.execute('select database();')
            cursor.execute(qr)

            connection.commit()

    except Error as e:
        print("Error 1024",e)

def read_table(qr):
    try:
        connection = mysql.connector.connect(host='localhost',database="Users",user="root",password='root')

        if connection.is_connected():
            db_info = connection.get_server_info()
            cursor = connection.cursor(buffered=True)
            cursor.execute('select database();')
            cursor.execute(qr)

            results = cursor.fetchall()

            for row in results:
                number = row[1]

            return number

    except Error as e:
        print("Error 1033",e)


key = 
bot = telebot.TeleBot(token=key)


@bot.message_handler(commands=['disconnect'])
def disconnect(message):
    userid=message.from_user.id
    bot.reply_to(message,u"Disconnecting from chat..")
    qr="DELETE FROM active_user WHERE number="+str(userid)+";"
    write_table(qr)
    connected=False
    os.remove(str(userid))
    bot.reply_to(message,u"Disconnected!")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,u"Hello, Let's get you a pigeon!")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,u"Sending a helper pigeon right this way...")

@bot.message_handler(commands=['connect'])
def connect(message):
    global connected,fname
    userid=message.from_user.id
    bot.reply_to(message,u"Sending a pigeon to search about the neighborhood...")
    qr="INSERT INTO active_user(number,ready) values("+str(userid)+",1);"
    write_table(qr)
    while(not connected):
        try:
            f=open(str(userid),"r")
            f.close()
            connected=True
        except IOError:
            pass
    bot.reply_to(message,u"Match found!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    userid=message.from_user.id
    if(connected):
        f=open(str(userid),"r")
        fcont=f.read().split(":")
        f.close()

        bot.send_message(int(fcont[0]),message.text)
bot.polling()
