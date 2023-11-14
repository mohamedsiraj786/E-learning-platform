import mysql.connector
from tabulate  import tabulate

conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
cursor = conn.cursor()


def Insert(name,contact,email):
    res = cursor
    query = "insert into users (username,contact,email) values(%s,%s,%s)"
    user_info = (name,contact,email)
    res.execute(query,user_info)
    conn.commit()
    print("Data Inserted Successfully")
    
def Update(userid,name,conatct,email):
    res = cursor
    query = "update users set username=%s,contact=%s,email=%s where user_id=%s"
    user_info = (name,conatct,email,userid)
    res.execute(query,user_info)
    conn.commit()
    print("Data Updated Successfully")
    
def Delete(userid):
    res = cursor
    query = "delete  from users where user_id=%s"
    user_info = (userid,)
    res.execute(query,user_info)
    conn.commit()
    print("Data Deleted Successfully")
    
def ViewData():
    res = cursor
    query = "select user_id,username,contact,email from users"
    cursor.execute(query)
    result = cursor.fetchall()
    print(tabulate(result,headers=["id","username","contact", "email"]))
    
    
while True:
     print("1.Insert Data") 
     print("2.Update Data") 
     print("3.Delete Data") 
     print("4.View Data") 
     print("5.Exit") 
     
     choose = int(input("Enter Your Choice : "))
     
     if choose == 1:
         name = input("Enter Username : ")
         contact = input("Enter Contact Number : ")
         email = input("Enter Email ID : ")
         Insert(name,contact,email)
         
     elif choose == 2:
          userid = input("Enter User ID : ")
          name = input("Enter Username : ")
          contact = input("Enter Contact Number : ")
          email = input("Enter Email ID : ")
          Update(userid,name,contact,email)
           
     elif choose == 3:
           userid = input("Enter User ID To Delete : ")
           Delete(userid)
           
     elif choose == 4:
           ViewData()
           
     elif choose == 5:
           break     
     
     else:
       print("Invalid Selection")   
             
       