# Swap Drop Enroll

Swap Drop Enroll is a utility that helps UNC students (who use this service) get their desired schedules. It uses sendgrid's webhook along with the Capybara webdriver to automatically enroll users into their classes. 

Since the first release, we have added numerous security features including an AES cipher. There are two of us working on this, and each of us will know one of the two encryption keys to actually access user password. This way, no individual member of our team can ever access a user password as a string.

Scheduled to launch in Fall 2016.

Built with Flask, Heroku and PhantomJS.
