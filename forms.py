import driver

goods = {
	"onyen": "ddfulton", 
	"course": "CHEM 261-001",
	"email": "ddfulton@live.unc.edu"
}

msg = """
Dear %s,\n

You just signed up for %s.

Welcome to Swap Drop Enroll. This service waits for an e-mail from classchecker, reads that email, 
and if the status changes from Closed to Open, it fetches your password and enrolls you. 

We use three layers of security to protect your password. If you are interested, 
we use a SOAP client with both a token and cipher, among other security features. 

Feel free to contact us at swapdropenroll@gmail.com.

Warm regards, 

Swap Drop Enroll
""" % (goods['onyen'], goods['course'])

driver.send_email(goods['email'], 'Swap Drop Enroll', msg)