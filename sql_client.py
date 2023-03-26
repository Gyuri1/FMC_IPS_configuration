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
  client= pymssql.connect("sql_server.mycompany.com:1433", "sqladmin", "BigSecret", "database_name")           
  cursor=client.cursor(as_dict=True)
 
  print("PRINT ALL with SELECT *") 
  call_sql("SELECT FROM TAJ:")

  print("print good ID:")
  call_sql("SELECT A FROM TAJ WHERE id='123456788';")

  print("print bad ID:")
  call_sql("SELECT A FROM TAJ WHERE id='11234567891';")

  client. close() 
  time.sleep(3) 
  print("\r")