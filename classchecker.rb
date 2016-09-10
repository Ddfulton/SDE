__author__ = "We'll never tell"

require 'capybara'
require 'capybara/poltergeist'

puts("INFO: SIGNING UP TO TRACK THE FOLLOWING WITH COURSICLE: %s" %(course))

course = ARGV[0]

session = Capybara::Session.new(:poltergeist)

session.visit "https://www.coursicle.com/notify/#unc"

session.find(:id, "alternateMethodLink").click()

session.find(:id, "emailInput").send_keys('inbound@registerer69.bymail.in')

session.find(:id, "classInputField1").send_keys(course)

session.find(:id, "notifyButton").click()