
def send_email_attachment(to, subject, text, attachment):
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from email.mime.base import MIMEBase
	from email import encoders
	 
	fromaddr = "registerer69@gmail.com"
	toaddr = to
	 
	msg = MIMEMultipart()
	 
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject
	 
	body = text
	 
	msg.attach(MIMEText(body, 'plain'))
	 
	filename = attachment
	attachment = open(attachment, "rb")
	 
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	 
	msg.attach(part)
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "bojangles1")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def send_email_plain(recipient, subject, text):
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	 
	 
	fromaddr = "registerer69@gmail.com"
	toaddr = recipient
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject
	 
	body = text
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "bojangles1")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


send_email_plain("fulton.derek@gmail.com", "SUBJECT", "FUCK YOU")