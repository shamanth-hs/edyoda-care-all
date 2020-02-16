from db import *
from profile import User
from younger_profile import YoungerProfile
from elder_profile import ElderProfile

# welcome note and giving oprion to login or register
def welcome():
    print("Please select\n1. Login as Elder \n2. Login as Younger\n3. Register\n4. View all youngers who are taking care\n5. View who is taking care of older couple\n6. Exit")
    task = int(input())
    if task==1:
        mobile = input("Welcome Elder\nEnter Your Email: ")
        password = input("Enter Your Password: ")
        user = ElderProfile(mobile, password)
        user.log_in()
    
    elif task==2:
        mobile = input("Welcome younger\nEnter Your Email: ")
        password = input("Enter Your Password: ")
        user = YoungerProfile(mobile, password)
        user.log_in()
    
    elif task==3:
        name = input("Register Yourself\nEnter Your Full Name: ")
        email = input("Enter your email: ")
        mobile = input("Enter Your Mobile Number: ")
        password = input("Enter Your Password: ")
        
        # if a user select wrong option it will ask again to select option
        while True:
            role = int(input("select your role:\n1. Elder\n2. Younger\n"))
            try:
                if role==1:
                    role="elder"
                    break
                elif role==2:
                    role="younger"
                    break
            except:
                print(f'option not Valid! Please try again')

        user_signup = User(name, email, password, mobile, role)
        user_signup.user_registration()
        
    # display name of youngers who are taking care of
    elif task==4:
        sql = '''SELECT `name` FROM users WHERE `PK_user_id` IN 
            (SELECT FK_user_id FROM `youngers` WHERE `PK_younger_id` IN 
            (SELECT `FK_younger_id` FROM elders))'''
        mycursor.execute(sql)
        user_data = mycursor.fetchall()
        for data in user_data:
            print(data)
        # pass

    # enter elder's mobile number of email both are unique here and display their take care name
    elif task==5:
        print("Enter elders email id to check their take cares name")
        email_id = input()
        sql1 = "SELECT `FK_user_id` FROM elders WHERE `FK_user_id` IN (SELECT `PK_user_id` FROM users WHERE email = %s);"
        val = (email_id)
        mycursor.execute(sql1,val)
        elder_id = mycursor.fetchall()
        if not elder_id:
            print("No Elder or User found with this mail id")
            welcome()
            return
        sql2 = "SELECT `FK_younger_id` FROM request WHERE `request_status` = 1  AND `FK_elder_id` = %d;"
        val2 = (elder_id)
        mycursor.execute(sql2,val2)
        names = mycursor.fetchall()
        for name in names:
            print(name)

    elif task==6:
        exit()

welcome()
