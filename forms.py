import driver

nextOnyen = 'ddfulton'
course = "ECON 101-007"

if nextOnyen != "NONE":
    # TODO Also get next e-mail
    onyenPassword = "bojangles5'"

    print("INFO: Enrolling %s in %s" % (nextOnyen, course))
    driver.enroll(nextOnyen, onyenPassword, course)
    print("INFO: Sending e-mail to fulton.derek@gmail.com")
    image_title = "%s_%s.png" % (nextOnyen, course)
    driver.send_email('fulton.derek@gmail.com', 'Your Swap Drop Enroll Result',
                      'just tried to enroll %s in %s.' % (nextOnyen, course), attachment=image_title)

    user_email = nextOnyen + "@live.unc.edu"

    driver.send_email(user_email, 'Your Swap Drop Enroll Result',
                      'Just tried to enroll %s in %s' % (nextOnyen, course), attachment=image_title)




    # if enrollment successful
    # zeep.markEnrollPass

    return_message = "Enrolled %s in %s" % (nextOnyen, course)

    print(return_message, 200)

else:
	print("INFO: nextOnyen is NONE")
	fail_message = "There was no nextOnyen for %s" % course
	print(return_message, 200)