from twilio.rest import Client #导包

account_sid = 'AC6f83a8e42f0112ba376f0a220954b26d'
auth_token = '900751559b244d20a506db1889a8ce30'

client = Client(account_sid, auth_token)

message = client.messages.create(
        from_ = '+12076790485',
        body = '欢迎关注一行数据',
        to = '+31613735290'
        )

print(message.sid)