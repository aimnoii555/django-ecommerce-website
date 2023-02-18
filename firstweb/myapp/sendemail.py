import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendthai(sendto,subj="ทดสอบส่งเมลลล์",detail="สวัสดี!\nคุณสบายดีไหม?\n"):

	myemail = 'moon0010010010@gmail.com'
	mypassword = 'aimnoii555'
	receiver = sendto

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subj
	msg['From'] = 'Admin Suksan Fruit'
	msg['To'] = receiver
	text = detail

	part1 = MIMEText(text, 'plain')
	msg.attach(part1)

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()

	s.login(myemail, mypassword)
	s.sendmail(myemail, receiver.split(','), msg.as_string())
	s.quit()


###########Start sending#############
subject = 'ยืนยันการสมัครเว็บไซต์ซื้อผลไม้ Suksan Fruit'

newmember_name = 'สมชาติ'
content = '''
เพื่อความปลอดภัยในการเข้าใช้ระบบ กรุณายืนยันอีเมล ผ่านลิ้งค์นี้
'''
link = 'http://www.suksan.lovestoblog.com'

msg = 'สวัสดีคุณ {} \n\n {} \n Verify link: {}'.format(newmember_name,content,link)

sendthai('moon0010010010@gmail.com',subject,msg)