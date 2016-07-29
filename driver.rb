require 'capybara'
require 'capybara/poltergeist'

def enroll(onyen, password, class1)
    start = Time.now

    session = Capybara::Session.new(:poltergeist)

    session.visit "https://connectcarolina.unc.edu/"
    session.find('.loginbutton').click()

    puts("LOGGING IN...\n")
    session.find('#onyen').send_keys('ddfulton')
    session.find('#onyenPassword').send_keys('bojangles5\'')
    session.find('#action').click() # breaks on heroku

    session.within_frame(session.find('#ptifrmtgtframe')) do
        session.find("#ACE_DERIVED_SSS_SCL_SSS_ENRL_CART").click()
    end

    puts("LOGGED IN")

    # Fall 2016 and Summer II 2016 Options — click fall 2016 if the table shows up
    session.within_frame(session.find('#ptifrmtgtframe')) do 
        begin
        	class_table = session.find('table.PSLEVEL2GRIDWBO')
       		fall_2016 = class_table.find('span', text: '2016 Fall')[:id]
        	fall_2016_idx = fall_2016[-1]
        	#puts(fall_2016_idx)
        
        	fall_2016_xpath = "//*[@id=\"trSSR_DUMMY_RECV1$0_row2\"]/td[1]"
        	# click fall 2016
        	session.find(:xpath, fall_2016_xpath).click(); #TODO Improve and adapt for no term select page

        	# click continue
        	session.find("a#DERIVED_SSS_SCT_SSR_PB_GO").click()
        rescue Capybara::ElementNotFound
        	puts("semester choice table did not come up")
        end
    end

    # works pretty well
    session.within_frame(session.find(:id, "ptifrmtgtframe")) do 
        cart = session.find("table.PSLEVEL1GRIDNBO")
        course = cart.find("a#P_CLASS_NAME\\$0")
        
        puts("wanted class:" + " " + class1)

        i = 0
        q=0

        #begin

        until q!=0 #while i > 0
        	begin
        		counter = "%s" %(i)
        		course = cart.find("a#P_CLASS_NAME\\$" + counter) 
        		puts("cart position:" + " " + counter)
        	
        		if course.text == class1 #course name equals name of the course in spot "i"
 
        			cart.find("input#P_SELECT\\$" + counter).click()
        			puts("found class:" + " " + cart.find("a#P_CLASS_NAME\\$" + counter).text)
        			q=1

        		else
        			puts("did not find")
        		end

        	rescue Capybara::ElementNotFound #change this so that it only applies to not being able to find spot in table, not just general "element not found"
        		puts("cart position:" + " " + counter)
        		puts $!, $@
        		puts("skipped spot due to recitation being there")
        	end

        i += 1
        end

        # rescue Capybara::ElementNotFound #change this so that it only applies to not being able to find spot in table, not just general "element not found"
        # 		puts("cart position:" + " " + counter)
        # 		puts("skipped spot due to recitation being there")
     	# end
        
        session.find("a#DERIVED_REGFRM1_LINK_ADD_ENRL").click()
        puts("clicked enroll")

        session.find("a#DERIVED_REGFRM1_SSR_PB_SUBMIT").click()
        puts("clicked finish enrolling")
    end
 
    finish = Time.now
    puts("\n\nTime to enroll:")
    puts(finish-start)

    sleep(3)
    session.save_screenshot('final.png')

end

enroll("ddfulton" , "bojangles5'" , "MATH 232-001 (2142)")
