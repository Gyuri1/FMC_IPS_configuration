import pymssql
import time

def call_sql(text):
    try:
        cursor.execute(text) 
        for row in cursor: 
            print (row)
    except Exception as err: 
        print("Connection problem")
         
for i in range(1000):
  client= pymssql.connect("sql.mycompany.com:1433", "sqladmin", "bigsecret", "DBname")           
  cursor=client.cursor(as_dict=True)
 
  print("PRINT * ALL with SELECT *") 
  call_sql("SELECT * FROM TAJ;")

  print("print good ID:")
  call_sql("SELECT * FROM TAJ WHERE taj='123456788';")

  print("print bad ID:")
  call_sql("SELECT * FROM TAJ WHERE taj='123456789';")

  client. close() 
  time.sleep(3) 
  print("\r")