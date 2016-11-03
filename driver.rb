
onyen = ARGV[0]
password = ARGV[1]
class1 = ARGV[2]

def enroll(onyen, password, class1)

    require 'capybara'
    require 'capybara/poltergeist'

    Capybara.javascript_driver = :poltergeist

    options = {js_errors: false}
    Capybara.register_driver :poltergeist do |app|
        Capybara::Poltergeist::Driver.new(app, options)
    end

    start = Time.now

    
    session = Capybara::Session.new(:poltergeist)



    ### Range for North Carolina IP Addresses: ###
    ### 24.40.128.0 - 24.40.160.0 ###

    ### X FORWARDED FOR HEADERS ### 
    headers = ['4.18.172.0', '4.137.72.0', '8.20.241.0', '12.27.251.0', 
        '12.53.254.0', '12.101.144.0', '4.18.168.0', '4.137.32.0',
        '4.138.20.0', '4.152.147.0', '12.1.242.0', '12.76.210.0', 
        '12.76.210.0', '4.154.8.0', '4.154.29.0', '12.70.250.0', 
        '12.234.11.0', '24.40.141.0', '24.40.200.0', '24.136.167.0',   
        '24.136.232.0', '24.162.230.0', '24.172.251.0', '24.211.255.0',
        '24.225.71.0', '64.102.200.0', '64.246.202.0', '65.40.172.0', 
        '65.190.184.0', '65.190.193.0', '66.57.36.0', '66.57.226.0', 
        '66.57.250.0', '66.193.208.0', '66.193.216.0', '66.202.135.0',
        '66.255.33.0', '68.221.114.0', '69.134.10.0', '69.134.26.0',
        '12.52.176.0', '24.211.228.0', '64.102.206.0', '65.167.183.0',
        '65.190.21.0', '65.190.41.0', '66.0.178.0', '66.192.165.0',
        '70.144.139.0']
        
    session.driver.headers = {'X-Forwarded-For' => headers.sample}

    session.visit "https://connectcarolina.unc.edu/"
    session.find('.loginbutton').click()

    puts("INFO: LOGGING IN...\n")

    session.find('#username').send_keys(onyen)
    session.find('#password').send_keys(password)
    session.find(:class, '.form-element.form-button').click()

    sleep(1)
    # Sometimes can't find this frame
    session.within_frame(session.find('#ptifrmtgtframe')) do
        session.find("#ACE_DERIVED_SSS_SCL_SSS_ENRL_CART").click()
    end

    puts("INFO: LOGGED IN")


    # NAVIGATE TO SHOPPING CART
    session.save_screenshot("debug.png")
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
                puts("Cart position: " + counter)
            
                if course.text.include? class1 # If it's the course we want
 
                    cart.find("input#P_SELECT\\$" + counter).click() # Click the fucker
                    puts("Found course:" + " " + cart.find("a#P_CLASS_NAME\\$" + counter).text)
                    

                    session.find("a#DERIVED_REGFRM1_LINK_ADD_ENRL").click()
                    session.save_screenshot("clicked enroll.png")
                    puts("Clicked 'enroll'")

                    # If no enrollment appointment, this returns you to shopping cart with no message.
                    begin
                        session.find("a#DERIVED_REGFRM1_SSR_PB_SUBMIT").click()
                        puts("Clicked 'finish enrolling'")
                        elapsed = Time.now - start
                        puts("%s seconds elapsed."%(elapsed))
                        break
                    rescue Capybara::ElementNotFound
                        puts("Did not find the 'finish enrolling' button")
                        elapsed = Time.now - start
                        puts("%s seconds elapsed."%(elapsed))
                        break
                    end


                else
                    puts("Course not in row " + counter)
                end

            rescue Capybara::ElementNotFound 
                puts("Cart position: " + " " + counter)
                
                puts("Skipped due to recitation")
                z += 1
                if z >= cart_elements.size
                    session.save_screenshot("class not in cart.png")
                    abort("Error: Class not in Shopping Cart!")
                end
            end
        end
    end


    image_title = "%s" %(onyen) + "_%s" %(class1) + ".png"

    sleep(5)
    session.save_screenshot(image_title)
end

### Call the function ###
enroll(onyen, password, class1)




