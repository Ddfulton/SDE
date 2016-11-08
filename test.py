import newClient
import base64
import bojangles
import pymysql
import driver

connection = newClient.DATABASE()

cursor = connection.cursor()

sql = 'select * from SDECheap.USERS;'

cursor.execute(sql)

todo = cursor.fetchall()

for i in todo:
    email = i["onyen"] + '@live.unc.edu'
    print(email)
    driver.send_email(email, "User Update", "Dear users,\n\nWe have changed the encryption process to make it more secure. All onyens registered before right now were encrypted differently than the current encryption algorithm would encrypt them. Therefore, they cannot be decrypted.\n\nYour entries have been deleted and you must sign up again so that the system may encrypt your password properly.\n\nIf you have any questions, please do not hesitate to contact us at blowjangles@protonmail.com.\n\nSorry for any inconvenience,\n\nSwap Drop Enroll")

connection.close()
