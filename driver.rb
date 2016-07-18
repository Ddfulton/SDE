require 'capybara'
require 'capybara/poltergeist'

def enroll_chem261(onyen, password)
    start = Time.now

    session = Capybara::Session.new(:poltergeist)

    session.visit "https://connectcarolina.unc.edu/"
    session.find('.loginbutton').click()

    puts("LOGGING IN...\n")
    session.find('#onyen').send_keys(onyen)
    session.find('#onyenPassword').send_keys(password)
    session.find('#action').click() # breaks on heroku

    session.within_frame(session.find('#ptifrmtgtframe')) do
        session.find("#ACE_DERIVED_SSS_SCL_SSS_ENRL_CART").click()
    end

    # Fall 2016 and Summer II 2016 Options — click fall 2016 if the table shows up
    session.within_frame(session.find('#ptifrmtgtframe')) do 
        class_table = session.find('table.PSLEVEL2GRIDWBO')
        fall_2016 = class_table.find('span', text: '2016 Fall')[:id]
        fall_2016_idx = fall_2016[-1]
        puts(fall_2016_idx)
        
        fall_2016_xpath = "//*[@id=\"trSSR_DUMMY_RECV1$0_row2\"]/td[1]"
        # click fall 2016
        session.find(:xpath, fall_2016_xpath).click(); #TODO Improve and adapt for no term select page

        # click continue
        session.find("a#DERIVED_SSS_SCT_SSR_PB_GO").click()
    end

    # works pretty well
    session.within_frame(session.find(:id, "ptifrmtgtframe")) do 
        cart = session.find("table.PSLEVEL1GRIDNBO")
        course = cart.find("input#P_SELECT\\$0")
        course.click()

        session.find("a#DERIVED_REGFRM1_LINK_ADD_ENRL").click()
        session.find("a#DERIVED_REGFRM1_SSR_PB_SUBMIT").click()
    end

    sleep(1)
    session.save_screenshot('final.png')

    finish = Time.now
    puts("\n\nTook you this long:")
    puts(finish-start)
end



enroll_chem261('ddfulton', "bojangles5'")