__author__ = "Derek Fulton"

require 'capybara'
require 'capybara/poltergeist'

course = ARGV[0]
puts("SIGNING UPT TO TRACK THE FOLLOWING WITH COURSICLE: %s" %(course))

session = Capybara::Session.new(:poltergeist)

puts("VISITING COURSICLE...")
session.visit "https://www.coursicle.com/notify/#untrack"

puts("CLICKING EMAIL...")
session.find(:id, "alternateMethodLink").click()

puts("FILLING BOX IN...")
session.find(:id, "emailInput").send_keys('inbound@registerer69.bymail.in')

puts("ENTERING COURSE")
session.find(:id, "classInputField1").send_keys(course)

puts("CLICKING NOTIFY...")
session.find(:id, "notifyButton").click()

