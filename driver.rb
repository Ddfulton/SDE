require 'capybara'
require 'capybara/poltergeist'
require 'sendgrid-ruby'
include SendGrid

def enroll(onyen, password, class1)
    start = Time.now

    session = Capybara::Session.new(:poltergeist)

    session.visit "https://connectcarolina.unc.edu/"
    session.find('.loginbutton').click()

    puts("LOGGING IN...\n")

    session.find('#username').send_keys('ddfulton')
    session.find('#password').send_keys('bojangles5\'')
    session.find(:class, '.form-element.form-button').click()

    session.within_frame(session.find('#ptifrmtgtframe')) do
        session.find("#ACE_DERIVED_SSS_SCL_SSS_ENRL_CART").click()
    end

    puts("LOGGED IN")


    # NAVIGATE TO SHOPPING CART
    session.within_frame(session.find('#ptifrmtgtframe')) do 
        begin
        	class_table = session.find('table.PSLEVEL2GRIDWBO')
       		fall_2016 = class_table.find('span', text: '2016 Fall')[:id]
        	fall_2016_idx = fall_2016[-1]
        
        	fall_2016_xpath = "//*[@id=\"trSSR_DUMMY_RECV1$0_row2\"]/td[1]"

        	session.find(:xpath, fall_2016_xpath).click();


        	session.find("a#DERIVED_SSS_SCT_SSR_PB_GO").click()

        rescue Capybara::ElementNotFound
        	puts("No Fall 2016/Summer II 2016 Choice Table")
        end
    end

    # LOOP THROUGH TABLE
    session.within_frame(session.find(:id, "ptifrmtgtframe")) do 
        
        cart = session.find("table.PSLEVEL1GRIDNBO") # Table
        
        course = cart.find("a#P_CLASS_NAME\\$0")
        
        puts("WANT:" + " " + class1)

        i = 0
        q = 0

        until q!=0 #while i > 0
        	begin
        		counter = "%s" %(i)
        		course = cart.find("a#P_CLASS_NAME\\$" + counter) 
        		puts("cart position:" + " " + counter)
        	
        		if course.text == class1 # If it's the course we want
 
        			cart.find("input#P_SELECT\\$" + counter).click() # Click the fucker
        			puts("Found course:" + " " + cart.find("a#P_CLASS_NAME\\$" + counter).text)
        			q = 1

        		else
        			puts("Course not in row " + counter)
        		end

        	rescue Capybara::ElementNotFound 
        		puts("Cart position: " + " " + counter)
        		puts $!, $@
        		puts("Skipped due to recitation")
        	end

        i += 1
        end

        
        session.find("a#DERIVED_REGFRM1_LINK_ADD_ENRL").click()
        puts("Clicked 'enroll'")

        session.find("a#DERIVED_REGFRM1_SSR_PB_SUBMIT").click()
        puts("Clicked 'finish enrolling'")
    end
 
    finish = Time.now

    puts("\n\nTime to enroll:")

    puts(finish-start)

    image_title = "%s" %(onyen) + "_%s" %(class1) + "_%s" %(finish) + ".png"

    session.save_screenshot(image_title)
end


def class_checker(course)
    session = Capybara::Session.new(:poltergeist)
    session.visit "https://www.coursicle.com/notify/#unc"

    session.find(:id, "alternateMethodLink").click()

    session.find(:id, "emailInput").send_keys('inbound@registerer69.bymail.in') # INBOUND PARSE
end

class_checker('CHEM 262-001')
