from db import *
import pdb

class ElderProfile():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        sql = f'SELECT PK_user_id, name FROM users WHERE email = "{self.email}" '
        mycursor.execute(sql)
        # pdb.set_trace()
        user_id = mycursor.fetchone()
        # pdb.inspect()
        # if user_id != None:
        try:
            self.user_id = user_id[0]
            self.elder_name = user_id[1]
            sql = f'SELECT PK_elder_id FROM elders WHERE FK_user_id={self.user_id}'
            mycursor.execute(sql)
            elder_id = mycursor.fetchone()
            self.elder_id=elder_id[0]
        except Exception:
            self.user_id = None
            self.elder_name = None
            # sql = f'SELECT PK_elder_id FROM elders WHERE FK_user_id={self.user_id}'
            # mycursor.execute(sql)
            # elder_id = mycursor.fetchone()
            self.elder_id=None

    def log_in(self):
        #retrieving passwords for registered mobile no from both table
        sql = f'SELECT password FROM users WHERE email= "{self.email}" '
        mycursor.execute(sql)
        user_info = mycursor.fetchone()     # fetchall provides empty list if record does not exists
        if user_info==[] or user_info == None:
            print(f'{self.email} not registered. Please try to register first')
            import index      # due to mutual importing we are importing here just before method calling
        elif self.password==user_info[0]:
            print("Logged IN")
            self.dashboard_elder()
        else:
            print("Wrong email and password")
            import index

    def dashboard_elder(self):
        sql = f'SELECT available FROM elders where PK_elder_id = {self.elder_id}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if user_info[0]==1:
            print("You are currently Available to take care of.\n1.Make Unavailable\n2.Fund\n3.Request\n4.Take Care Name\n5.Give review and rating for a younger\n6.LogOut")
            choice = int(input())
            if choice==1:
                self.change_status(0)
                self.dashboard_elder()
            elif choice==2:
                self.allocate_fund()
            elif choice==3:
                self.show_request()
            elif choice==4:
                self.take_care_name()
            elif choice==5:
                self.review()
            elif choice==6:
                self.log_out()

        else:
            print("You are currently Unavailable to take care of.\n1.Make Available\n2.Log Out")
            choice = int(input())
            if choice==1:
                self.change_status(1)
                self.dashboard_elder()
            elif choice==2:
                self.log_out()

    # elder should be able to allocate fund
    def allocate_fund(self):
        fund =  int(input("Enter the fund to be allocated: "))
        if fund == None or fund == 0:
            fund =  int(input("fund cannot be 0 or empty enter again or press 0 to exit: "))
            if fund == 0:
                self.dashboard_elder()
        sql = "UPDATE elders set fund = %s WHERE PK_elder_id = %s"
        val = ( fund, self.elder_id)
        mycursor.execute(sql, val)
        self.dashboard_elder()

    # elder can change their status from available to unavailable and vice-versa
    def change_status(self,value):
        sql = "UPDATE elders set available = %s WHERE PK_elder_id = %s"
        val = ( value, self.elder_id)
        if(mycursor.execute(sql, val)):
            print("status Changed Successfully")
            self.dashboard_elder()
        else:
            print("Database error")
            self.dashboard_elder()

    # elder can see requests and accept whome they trus only 1 request can be accepted by elder      
    def show_request(self):
         sql = '''select '''

    # elder can see name of younger who is taking care of them
    def take_care_name(self):
        sql = '''SELECT `name` FROM users WHERE `PK_user_id` = 
        (SELECT `FK_user_id` FROM `youngers` WHERE `PK_younger_id` = 
        (SELECT `FK_younger_id` FROM `elders` WHERE `PK_elder_id` = %d))'''
        val = (self.elder_id)
        mycursor.execute(sql,val)
        care_taker = mycursor.fetchall()
        print(care_taker)
        # pass

    # elder can give review and rating to youngers
    def review(self):
        review = input("Please enter your review")
        ratings = int(input("Enter rating in range 0 to 10"))
        sql = 'SELECT `FK_user_id` FROM `youngers` WHERE `PK_younger_id` = (SELECT `FK_younger_id` FROM `elders` WHERE `PK_elder_id` = %d)'
        val = (self.elder_id)
        mycursor.execute(sql,val)
        care_taker_id = mycursor.fetchall()
        review_query = 'INSERT INTO `reviews` (`FK_user_id`,`review`,`rating`,`review_by`) VALUES (%d,%s,%d,%s)'
        vals = (care_taker_id,review,ratings,self.elder_name)
        try:
            mycursor.execute(review_query,vals)
            print("review updated")
            self.dashboard_elder()
        except Exception:
            print("Error")
            

    def log_out(self):
        import index
