from db import *

class YoungerProfile():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        sql = f'SELECT PK_user_id, name FROM users WHERE email = "{self.email}" '
        mycursor.execute(sql)
        user_id = mycursor.fetchone()
        self.user_id = user_id[0]
        self.younger_name = user_id[1]
        sql = f'SELECT PK_younger_id FROM youngers WHERE FK_user_id={self.user_id}'
        mycursor.execute(sql)
        younger_id = mycursor.fetchone()
        self.younger_id=younger_id[0]
        sql = f'SELECT FK_younger_id from elders where FK_younger_id = {self.younger_id}'
        mycursor.execute(sql)
        self.youngerCount = mycursor.fetchall()

    def log_in(self):
        #retrieving passwords for registered mobile no from both table
        sql = f'SELECT password FROM users WHERE email= "{self.email}" '
        mycursor.execute(sql)
        user_info = mycursor.fetchone()     # fetchall provides empty list if record does not exists
        if user_info==[]:
            print(f'{self.email} ot registered. Please try to register first')
            import index      # due to mutual importing we are importing here just before method calling
        elif self.password==user_info[0]:
            print("Logged IN")
            self.dashboard_younger()
        else:
            print("Wrong email and password")
            import index

    def dashboard_younger(self):
        elderCount = len(self.youngerCount)
        print(f'Currentlty you are taking care of {elderCount} Elders\nYou can request for {4-elderCount} more elders to take care of.\n1.View list of Available elders to take care of.\n2.Give review and rating for a elder\n3.LogOut')
        choice = int(input())
        if choice==1:
            self.request_elder()
        elif choice==2:
            self.review()
        elif choice==3:
            self.log_out()

    # user should be able to see list of available elder and sent them request. NOTE:- 1 user can't sent request to same elder twice
    def request_elder(self):
        sql = f'''SELECT PK_user_id,`name` FROM users,elders 
        WHERE users.PK_user_id = elders.FK_user_id AND
        available = 1'''
        mycursor.execute(sql)
        user_info = mycursor.fetchall()
        for user in user_info:
            print(user[0],user[1])
        elder_id = int(input("Enter Elder id to request"))
        sql1 = f'SELECT * FROM request WHERE FK_younger_id = {self.younger_id} AND FK_elder_id = {elder_id}'
        val =(self.younger_id,elder_id)
        mycursor.execute(sql1)
        data = mycursor.fetchall()
        if data == None or data == []:
            query = "INSERT INTO request (FK_younger_id,FK_elder_id,request_status) VALUES (%s,%s,0)"
            values = (self.younger_id,elder_id)
            if(mycursor.execute(query,values)):
                print("Request has been sent to the elder waiting for their aproval")
                self.dashboard_younger()
            else:
                print("Cannot perform request please try again later")
        else:
            print("You have already requested for this following elder")
            self.dashboard_younger()


    # younger can give rating and rating to elders
    def review(self):
        review = input("Please enter your review")
        ratings = int(input("Enter rating in range 0 to 10"))
        # change this query
        sql = 'SELECT `FK_user_id` FROM elders WHERE `PK_elder_id` = (SELECT `PK_elder_id` FROM elders WHERE `FK_younger_id` = %d)'
        val = (self.younger_id)
        mycursor.execute(sql,val)
        care_taker_id = mycursor.fetchall()
        review_query = 'INSERT INTO `reviews` (`FK_user_id`,`review`,`rating`,`review_by`) VALUES (%d,%s,%d,%s)'
        vals = (care_taker_id,review,ratings,self.younger_name)
        try:
            mycursor.execute(review_query,vals)
            print("review updated")
            self.dashboard_younger()
        except Exception:
            print("Error")


    def log_out(self):
        import index
