import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  use_pure=True,
  database="caregiving"
)
mycursor = mydb.cursor()

sql = f'''SELECT PK_user_id,`name` FROM users,elders 
WHERE users.PK_user_id = elders.FK_user_id AND
available = 1;'''
sql = f'SELECT `PK_request_id` FROM `request` WHERE`FK_younger_id`IN(SELECT `PK_younger_id` FROM `youngers` WHERE `FK_user_id` = "{}")'.format(3)
vals = (3)
mycursor.execute(sql)
user_info = mycursor.fetchall()
for user in user_info:
    print(user[0],user[1])