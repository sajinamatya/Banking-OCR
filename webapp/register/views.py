from django.shortcuts import render
import mysql.connector as sql

first_name = ""
last_name = ""
Email = ""
Password = ""
# Create your views here.
def register_user(request) : 
    global first_name,last_name,email,password
    if request.method == "POST":
        mysql = sql.connect(host="localhost",user="root",passwd = "", database="fyp")
        cursor = mysql.cursor()
        d = request.POST
        for key,value in d.items():
            if key == "first_name":
                first_name = value
            if key == "last_name":
                last_name = value
            if key == "Email":
                email = value
            if key == "Password":
                password = value
        sql_code = "insert into fyp values('{}','{}','{}','{}')".format(Email,first_name,last_name,Password)
        cursor.execute(sql_code)
        mysql.commit()
    
    return render(request,'register.html')