require 'sendgrid-ruby'
require 'mail'

sendgrid = SendGrid::Client.new do |c|
  c.api_key = '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'
end

email = SendGrid::Mail.new do |m|
  m.to      = 'fulton.derek@gmail.com'
  m.from    = 'you@youremail.com'
  m.subject = 'Sending with SendGrid is Fun'
  m.html    = 'and easy to do anywhere, even with Ruby'
end

sendgrid.send(email)





