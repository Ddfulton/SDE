require 'capybara'
require 'capybara/poltergeist'

onyen = ARGV[0]
password = ARGV[1]

# Range for North Carolina IP Addresses: 24.40.128.0 - 24.40.160.0
session = Capybara::Session.new(:poltergeist)



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
    '66.255.33.0', '68.221.114.0', '69.134.10.0', '69.134.26.0']

session.driver.headers = {'X-Forwarded-For' => headers.sample}

### LOG IN ###
session.visit "https://connectcarolina.unc.edu/"
session.find('.loginbutton').click()


begin
	session.find('#username').send_keys(onyen)
	session.find('#password').send_keys(password)
	session.find(:class, '.form-element.form-button').click()

	session.within_frame(session.find('#ptifrmtgtframe')) do
	    session.find("#ACE_DERIVED_SSS_SCL_SSS_ENRL_CART").click()
	end
rescue Capybara::ElementNotFound
	puts("NO")
else
	puts("YE")
end
