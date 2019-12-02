import mysql.connector
from mysql.connector import Error
import random
    
try:
    connection = mysql.connector.connect(host='localhost',database='Users',user='root',password='root')

    if connection.is_connected():
        db_info = connection.get_server_info()
        cursor = connection.cursor(buffered=True)
        cursor.execute('select database();')


        qr="SELECT NUMBER FROM active_user where ready=1;"
        cursor.execute(qr)

        results=cursor.fetchall()

        indx=random.randint(0,len(results)-1)

        user1=results[indx][0]

        qr="UPDATE active_user SET ready=0 where number="+str(user1)+";"
        cursor.execute(qr)
        connection.commit()

        qr="SELECT NUMBER FROM active_user where ready=1;"
        cursor.execute(qr)

        results=cursor.fetchall()

        indx=random.randint(0,len(results)-1)

        user2=results[indx][0]

        qr="UPDATE active_user SET ready=0 where number="+str(user2)+";"
        cursor.execute(qr)
        connection.commit()

        f=open(str(user1),"w")
        f.write(str(user2)+":2")
        f.close()

        f=open(str(user2),"w")
        f.write(str(user1)+":1")
        f.close()

        f=open(str(user1)+str(user2)+"BUFFER","w")
        f.close()



except Error as e:
    print("Error 1024",e)
