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

emails = []



for i in todo:
    email = i["onyen"] + '@live.unc.edu'
    if email in emails:
        pass
    else:
        print("Sending to %s" % email)
        emails.append(email)
        msg = "Dear %s,\n\nThank you for signing up for Swap Drop Enroll! As some of you may know, Swap Drop Enroll is a brand new tool that will help you and your friends get into the classes that you want.\n\nOf course, as a relatively new program, we are still looking to refine and optimize the user experience and design of Swap Drop Enroll. If you have any suggestions, complaints, or ideas for future improvements, we would love to know!\n\nSend us an email at blowjangles@protonmail.com to let us know how we can make Swap Drop Enroll a more intuitive, streamlined, and aesthetically spectacular experience for you and your loved ones. If you do, there just might be a few referral points thrown your way.\n\nRegards,\n\nSwap Drop Enroll Team" % (i["onyen"])
        driver.send_email(email, "Feedback", msg)


connection.close()
