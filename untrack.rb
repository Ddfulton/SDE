__author__ = "Derek Fulton"

require 'capybara'
require 'capybara/poltergeist'

course = ARGV[0]
puts("INFO: Untracking %s" %(course))

session = Capybara::Session.new(:poltergeist)

puts("VISITING COURSICLE...")
session.visit "https://www.coursicle.com/notify/#unc"

puts("CLICKING UNTRACK")
session.find(:id, "untrackNavItem").click()

puts("FILLING IN E-MAIL")
session.find(:id, "alternateMethodLink").click()
session.find(:id, "emailInput").send_keys("inbound@registerer69.bymail.in")

puts("FILLING IN CLASS")
session.find(:id, "classInputField1").send_keys(course)
session.find(:id, "notifyButton").click()

