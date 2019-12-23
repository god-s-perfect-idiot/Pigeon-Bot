import os
import telebot
import mysql.connector
from mysql.connector import Error


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
            return results

    except Error as e:
        print("Error 1033",e)


key = 
bot = telebot.TeleBot(token=key)


@bot.message_handler(commands=['disconnect'])
def disconnect(message):
    connected=False
    userid=message.from_user.id
    qr="SELECT * from connected where connector="+str(userid)+";"
    results=read_table(qr);
    if(len(results)>0):
        connected=True
        user2=results[0][1]
    if(connected):
        bot.reply_to(message,u"Disconnecting from chat..")

        qr="DELETE FROM active_user WHERE number="+str(userid)+";"
        write_table(qr)

        qr="DELETE FROM active_user WHERE number="+str(user2)+";"
        write_table(qr)

        qr="DELETE FROM connected WHERE connector="+str(userid)+";"
        write_table(qr)

        qr="DELETE FROM connected WHERE connector="+str(user2)+";"
        write_table(qr)

        bot.send_message(int(user2),u"Woops, the other User disconnected!")
        bot.reply_to(message,u"Disconnected!")
    else:
        bot.reply_to(message,u"You're not connected yet!")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,u"Hello, Let's get you a pigeon!\nAvailable commands and Usages:\n1./connect:\n\t/connect Male\n\t/connect male\n\t/connect Female\n\t/connect female\n2./disconnect\n3./start\n4./help\n5./report")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,u"Sending a helper pigeon right this way...")

@bot.message_handler(commands=['connect'])
def connect(message):
    userid=message.from_user.id
    qr="SELECT * FROM active_user where number="+str(userid)+";"
    results=read_table(qr)
    result=1
    if(len(results)==0):
        result=0
    if(result==0):
        qr="SELECT * FROM banlist WHERE number="+str(userid)+";"
        results=read_table(qr)
        safe=True
        if(len(results)>0):
            if(results[0][2]==3):
                safe=False
        if(safe):
            m_content=message.text.split()
            if(len(m_content)>1):
                if(m_content[1]=="Male" or m_content[1]=="male"):
                    bot.reply_to(message,u"Alright, "+m_content[1]+" it is!")
                    bot.send_message(userid,u"Sending a pigeon to search about the neighborhood...")
                    qr="INSERT INTO active_user(number,gender,ready) values("+str(userid)+",'Male',1);"
                    write_table(qr)
                elif(m_content[1]=="Female" or m_content[1]=="female"):
                    bot.reply_to(message,u"Alright, "+m_content[1]+" it is!")
                    bot.send_message(userid,u"Sending a pigeon to search about the neighborhood...")
                    qr="INSERT INTO active_user(number,gender,ready) values("+str(userid)+",'Female',1);"
                    write_table(qr)
                else:
                    bot.reply_to(message,u"59, 60, 61.. \nOkay, we're not 63 genders yet!")
            else:
                bot.reply_to(message,u"Okay, this won't work unless you tell me your gender!")
        else:
            bot.reply_to(message,u"Sorry, but you're BANNED!!!")
    else:
        bot.reply_to(message,u"Already in the wait queue, silly!")

@bot.message_handler(commands=['report'])
def ban(message):
    connected=False
    userid=message.from_user.id
    try:
        qr="SELECT * from connected where connector="+str(userid)+";"
        results=read_table(qr);
        if(len(results)>0):
            connected=True
            user2=results[0][1]
    except IOError:
        pass
    if(connected):
        qr="SELECT * FROM banlist WHERE number="+str(user2)+";"
        results=read_table(qr)
        if(len(results)>0):
            qr="UPDATE banlist SET warncount=warncount+1 WHERE number="+str(user2)+";"
            write_table(qr)
        else:
            qr="INSERT INTO banlist(number,warncount) VALUES("+str(user2)+","+"1);"
            write_table(qr)
        bot.reply_to(message,u"Hey, we'll keep this between us. But, that is dealt with.")
        disconnect(message)

    else:
        bot.reply_to(message,"No one to Report?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    connected=False
    userid=message.from_user.id
    try:
        qr="SELECT * from connected where connector="+str(userid)+";"
        results=read_table(qr);
        if(len(results)>0):
            connected=True
            user2=results[0][1]
    except IOError:
        pass
    if(connected):
        bot.send_message(int(user2),message.text)

bot.polling()
