require 'sendgrid-ruby'
require 'ruby_http_client'

include SendGrid

from = Email.new(email: 'test@example.com')
subject = 'Hello World from the SendGrid Ruby Library!'
to = Email.new(email: 'fulton.derek@gmail.com')
content = Content.new(type: 'text/plain', value: 'Hello, Email!')
mail = Mail.new(from, subject, to, content)

sg = SendGrid::API.new(api_key: ENV['XwenEGkCTOq3WrPLRI0k_A'])
response = sg.client.mail._('send').post(request_body: mail.to_json)
puts response.status_code
puts response.body
puts response.headers