import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import time

connection = mysql.connector.connect(host='localhost',
                             database='users_data',
                             user='root',
                             password='')

mycursor = connection.cursor()

param1 = []
param2 = 0
param3 = param2+1000

counter = 0

mycursor.execute("SELECT DISTINCT (TIME) FROM data_info")
a = mycursor.fetchall()
ind =1
for row in a:
    if(ind<=288):
        #print(ind)
        #print (row[0])
        param1.append(row[0])
        ind+=1

for timezone in param1:

    for count in range(0,10):#cover all steps - since they increase by 1000 (from 0 to 10000)
        sum = 0#sum of the steps at the specific hour
        summation = 0#sum of the final steps at the specific range
        mycursor.execute("SELECT VALUE FROM data_info WHERE TIME = %s AND FINALDAYSTEPS > %s AND FINALDAYSTEPS < %s", (timezone, param2, param3))
        lista = mycursor.fetchall()
        print("Values of days at the specific time:")
        print(timezone)
        print("And a specific range:")
        print(param2, param3)

        for i in lista:
            print("Value:", i)
            sum+=i[0]

        dividor = len(lista)
        print("dividor", dividor)
        print("sum", sum)
        if(dividor is not 0):
            
            avg_steps = sum/dividor
            print("average steps", avg_steps)



            data = (avg_steps, timezone, param2, param3)
            sqlq = "UPDATE data_info SET `FINAL_VALUE`= %s  WHERE TIME = %s AND FINALDAYSTEPS > %s AND FINALDAYSTEPS < %s"
            mycursor.execute(sqlq, data)
            connection.commit()


            mycursor.execute("SELECT FINALDAYSTEPS FROM data_info WHERE TIME = %s AND FINALDAYSTEPS > %s AND FINALDAYSTEPS < %s", (timezone, param2, param3))
            listaa = mycursor.fetchall()

            for finali in listaa:
                print("Value:", finali)
                summation+=finali[0]

            dividor1 = len(listaa)
            print("dividor", dividor1)
            print("summation", summation)
            avg_steps1 = summation/dividor1
            print("average steps final", avg_steps1)


            data = (avg_steps1, timezone, param2, param3)
            sqlq = "UPDATE data_info SET `FINALDAYSTEPS`= %s  WHERE TIME = %s AND FINALDAYSTEPS > %s AND FINALDAYSTEPS < %s"
            mycursor.execute(sqlq, data)
            connection.commit()

            param2+=1000
            param3 = param2+1000

            if(param3>10000):
                param2=0
                param3=1000
                continue
            print()
            print()
            print("END OF SPECIFIC TIME AND RANGE!")
            time.sleep(1)

        else:
            print("erorr")
            param2+=1000
            param3 = param2+1000

            if(param3>10000):
                param2=0
                param3=1000
                continue
            print()
            print()
            print("END OF SPECIFIC TIME AND RANGE!")
            time.sleep(1)
