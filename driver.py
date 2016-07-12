# MOst important: add the fuckers to class checker
# Decrement priority
# Second most important: Protect passwords
# Second most important: Make sure folks get notified when they start
# Deal with it if it's not in the cart!
# Third most important: Find a way to check if they got in or not. Detailed status report.
# Third most important: Recitations etc
# H12 request timeout
# Deprecate priorities
# TODO: Put imports at top
# TODO: Swap drop enroll
# TODO: Spinner and checkmark when submit
# TODO: Honors classes
# TODO: Fix sleep(1)

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep, time
import json, http.client
import sendgrid

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


def sendgridemail(recipient, body="DEFAULT BODY ARG", picture=False):
  client = sendgrid.SendGridClient("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")

  recipient = "<" + recipient + ">"

  message = sendgrid.Mail()
  message.add_to('Derek Fulton' + recipient)
  message.set_subject('Example')
  message.set_html(body)
  message.set_text(body)
  message.set_from('Enroll Ninja <enroll@ninjan.com>')




  if picture == True:
    message.add_attachment('templates/images/ss.png', './templates/images/ss.png')
  else:
    pass

  status, msg = client.send(message)
  return status, msg

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

