from songline import Sendline

token = 'oJry2bPLmFQlr3CS3csxU0U0oJxz9heTc76pWrnMKoS'

messenger = Sendline(token)

#test send
# messenger.sendtext('ว่าไง')
#messenger.sticker(13,1,'test')
messenger.sendimage('https://pixy.org/src/470/4705358.jpg')