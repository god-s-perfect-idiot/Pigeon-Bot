import mysql.connector
from mysql.connector import Error
import random
import telebot

key = "999816153:AAEPIqQrSBUkQiOv4ce60yz9u3tG_qJhqNU"
bot = telebot.TeleBot(token=key)

while(1):
    try:
        connection = mysql.connector.connect(host='localhost',database='Users',user='root',password='root')

        if connection.is_connected():
            db_info = connection.get_server_info()
            cursor = connection.cursor(buffered=True)
            cursor.execute('select database();')


            qr="SELECT NUMBER FROM active_user where ready=1 and gender='Male';"
            cursor.execute(qr)

            results=cursor.fetchall()

            if(len(results)>=1):

                if(len(results)>1):
                    indx=random.randint(0,len(results)-1)
                else:
                    indx=0

                user1=results[indx][0]

                qr="SELECT NUMBER FROM active_user where ready=1 and gender='Female';"
                cursor.execute(qr)

                results=cursor.fetchall()

                if(len(results)>=1):
                    if(len(results)>1):
                        indx=random.randint(0,len(results)-1)
                    else:
                        indx=0

                    user2=results[indx][0]
                    qr="UPDATE active_user SET ready=0 where number="+str(user2)+";"
                    cursor.execute(qr)
                    connection.commit()

                    qr="UPDATE active_user SET ready=0 where number="+str(user1)+";"
                    cursor.execute(qr)
                    connection.commit()

                    qr="INSERT INTO connected (connector,connectee) value("+str(user1)+","+str(user2)+");"
                    cursor.execute(qr)
                    connection.commit()
                    bot.send_message(user1,"Match found!")

                    qr="INSERT INTO connected (connector,connectee) value("+str(user2)+","+str(user1)+");"
                    cursor.execute(qr)
                    connection.commit()
                    bot.send_message(user2,"Match found!")



    except Error as e:
        print("Error 1024",e)
