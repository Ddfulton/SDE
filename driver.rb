require 'capybara'
require 'capybara/poltergeist'

puts("driver.rb IS IN BUSINESS")

onyen = ARGV[0]
password = ARGV[1]
class1 = ARGV[2]

def enroll(onyen, password, class1)
    start = Time.now


    # Range for North Carolina IP Addresses: 24.40.128.0 - 24.40.160.0
    session = Capybara::Session.new(:poltergeist)
    


    ### X FORWARDED FOR ### 
    headers = ['4.18.172.0', '4.137.72.0', '8.20.241.0', '12.27.251.0', 
        '12.53.254.0', '12.101.144.0', '4.18.168.0', '4.137.32.0',
        '4.138.20.0', '4.152.147.0', '12.1.242.0', '12.76.210.0', 
        '12.76.210.0', '4.154.8.0', '4.154.29.0', '12.70.250.0', 
        '12.234.11.0', '24.40.141.0', '24.40.200.0', '24.136.167.0',   
        '24.136.232.0', '24.162.230.0', '24.172.251.0', '24.211.255.0',
        '24.225.71.0', '64.102.200.0', '64.246.202.0', '65.40.172.0', 
        '65.190.184.0', '65.190.193.0', '66.57.36.0', '66.57.226.0', 
        '66.57.250.0', '66.193.208.0', '66.193.216.0', '66.202.135.0',
        '66.255.33.0', '68.221.114.0', '69.134.10.0', '69.134.26.0']
    

    session.driver.headers = {'X-Forwarded-For' => headers.sample}
    





    session.visit "https://connectcarolina.unc.edu/"
    session.find('.loginbutton').click()

    puts("LOGGING IN...\n")

    session.find('#username').send_keys(onyen)
    session.find('#password').send_keys(password)
    session.find(:class, '.form-element.form-button').click()

    sleep(3)
    session.visit "https://cs.cc.unc.edu/psc/campus/EMPLOYEE/UNC_CS/c/NC_CUSTOM_MENU.NC_PORTAL_STUDENT.GBL?PortalActualURL=https\%3a\%2f\%2fcs.cc.unc.edu\%2fpsc\%2fcampus\%2fEMPLOYEE\%2fUNC_CS\%2fc\%2fNC_CUSTOM_MENU.NC_PORTAL_STUDENT.GBL&PortalRegistryName=EMPLOYEE&PortalServletURI=https\%3a\%2f\%2fpa.cc.unc.edu\%2fpsp\%2fpaprd\%2f&PortalURI=https\%3a\%2f\%2fpa.cc.unc.edu\%2fpsc\%2fpaprd\%2f&PortalHostNode=EMPL&NoCrumbs=yes"
    sleep(3)
    

    puts("LOGGED IN")

    sleep(3)
    session.save_screenshot('debug.png')
    # NAVIGATE TO SHOPPING CART
    session.within_frame(session.find('#ptifrmtgtframe')) do 
        begin
        	class_table = session.find('table.PSLEVEL2GRIDWBO')
       		fall_2016 = class_table.find('span', text: '2016 Fall')[:id]
        	fall_2016_idx = fall_2016[-1]
        
        	fall_2016_xpath = "//*[@id=\"trSSR_DUMMY_RECV1$0_row2\"]/td[1]"

        	session.find(:xpath, fall_2016_xpath).click(); #TODO Improve and adapt for no term select page


        	session.find("a#DERIVED_SSS_SCT_SSR_PB_GO").click()

        rescue Capybara::ElementNotFound
        	puts("No Fall 2016/Summer II 2016 Choice Table")
        end
    end

    # LOOP THROUGH TABLE
    session.within_frame(session.find(:id, "ptifrmtgtframe")) do 
        puts("WANT:" + " " + class1)
        cart = session.find("table.PSLEVEL1GRIDNBO") # Table
        
        cart_elements = Array.new

        cart_elements = cart.all('tr')

        puts("There are %s in the cart" % cart_elements.size)

        i = 0
        q = 0
        z = 0


    
        for i in 1..cart_elements.size
            i = i - 1
        	begin
        		counter = "%s" %(i)
        		course = cart.find("a#P_CLASS_NAME\\$" + counter) 
        		puts("cart position:" + " " + counter)
        	
        		if course.text.include? class1 # If it's the course we want
 
        			cart.find("input#P_SELECT\\$" + counter).click() # Click the fucker
        			puts("Found course:" + " " + cart.find("a#P_CLASS_NAME\\$" + counter).text)
        			

                    session.find("a#DERIVED_REGFRM1_LINK_ADD_ENRL").click()
                    puts("Clicked 'enroll'")

                    session.find("a#DERIVED_REGFRM1_SSR_PB_SUBMIT").click()
                    puts("Clicked 'finish enrolling'")


                    break

        		else
        			puts("Course not in row " + counter)
        		end

        	rescue Capybara::ElementNotFound 
        		puts("Cart position: " + " " + counter)
        		
        		puts("Skipped due to recitation")
        		z += 1
        		if z >= cart_elements.size
        			abort("Error: Class not in Shopping Cart!")
        		end
        	end

        
        end

        
        
    end
 
    finish = Time.now

    puts(finish-start)

    image_title = "%s" %(onyen) + "_%s" %(class1) + ".png"

    sleep(5)
    session.save_screenshot(image_title)

   


end
enroll(onyen, password, class1)


