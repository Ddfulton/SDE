# Swap Drop Enroll

Swap Drop Enroll is a utility that helps UNC students (who use this service) get their desired schedules. It uses sendgrid's webhook along with the Capybara webdriver to automatically enroll users into their classes. 

Since the first release, we have added numerous security features including an AES cipher. This way, no individual member of our team can ever access a user password as a string.

Was shut down by UNC ITS late Spring 2017, unfortunately. 

Built with Flask, SQL, PhantomJS and Capybara.

# How to run locally

Make sure you have Python 3, virtualenv and pip installed on your machine. Then clone the repo and run:

~~~pip install -r requirements.txt~~~

~~~python swap.py~~~ 

This will run it locally on your machine.
