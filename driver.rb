require 'capybara'
require 'capybara/poltergeist'

start = Time.now

session = Capybara::Session.new(:poltergeist)

session.visit "https://connectcarolina.unc.edu/"
session.find('.loginbutton').click()

puts("LOGGING IN...\n")
session.find('#onyen').send_keys('ddfulton')
session.find('#onyenPassword').send_keys('bojangles5\'')
session.find('#action').click() # breaks on heroku

puts("ENTERING SHOPPING CART...\n")
#ENTER SHOPPING CART
session.within_frame(session.find('#ptifrmtgtframe')) do
    y = session.find("#ACE_DERIVED_SSS_SCL_SSS_ENRL_CART").click()
end

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

#LIST OF CLASSES
session.within_frame(session.find(:name, 'TargetContent')) do 
    
    class_table = session.find("table.SSSGROUPBOXDKBLUE") # works
    puts(class_table.methods.sort)

    #pertinent row ID is trSSR_REGFORM_VW$0_row1 (where 1 is any number)
    i = 1
    while class_table.find("tr#trSSR_REGFORM_VW$0_row" + i.to_s)
        puts("Found row number %i", i)
    end

end













finish = Time.now
puts("\n\nTook you this long:")
puts(finish-start)