
from time import sleep, time
import json
import sendgrid
from sendgrid.helpers.mail import *
import os


def classchecker(course="CHEM 262-001", email='registerer69@gmail.com', driver="PhantomJS()"): # not tested 6-1-16
  import time
  
  if driver == "PhantomJS()":
    driver = webdriver.PhantomJS()
  else:
    driver = webdriver.Firefox()
  driver.get("http://classchecker.com/")


  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#beginSignUp"))
    ).click()


  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#name_continue_button"))
  ).click()
  

  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#email_button"))
  ).click()


  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#email_input"))
  ).send_keys("registerer69@gmail.com")


  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#email_continue"))
  ).click()


  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#class_input_field1"))
  ).send_keys(course)


  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#submit_button"))
  ).click()

  picture = 'templates/images/classchecker.png' # Hard coded
  driver.save_screenshot(picture)
  text = "Just signed up for %s on classchecker" % (course)
  result = sendgridemail(email, body=text, picture=True)
  return result


def sendgridemail(): # broken
  
  sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('XwenEGkCTOq3WrPLRI0k_A'))
  from_email = Email("fuck@yo.u")
  subject = "Hello World from the SendGrid Python Library"
  to_email = Email("fulton.derek@gmail.com")
  content = Content("text/plain", "Fuck you")
  mail = Mail(from_email, subject, to_email, content)
  response = sg.client.mail.send.post(request_body=mail.get())
  print(response.status_code)
  print(response.body)
  print(response.headers)


def get_course(text):
  #TODO: Validate email text
  return text[0:12]

def get_status(text):
  text = text.lower()
  if "losed." in text: # period at end, so it's now closed
    return "closed"
  if "tracked" in text:
    return "tracked"
  else:
    return "open"

