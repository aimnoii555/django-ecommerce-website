from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, get_user, login
from django.contrib.auth.models import User
from datetime import datetime
from django.core.paginator import Paginator
import random


# Line Notify
from songline import Sendline
token = 'lSuSx5e4t7hK1hcPTz5Pqt3gDsvwquEXtIuv9rMkcbm'
messenger = Sendline(token)

#-------------------------Genterate Token--------------------------------------

def GenerateToken(domain='http://localhost:8000/confirm/'):
    allchar = [  chr(i) for i in range(65,91)]
    allchar.extend([chr(i) for i in range(97,123)])
    allchar.extend([str(i) for i in range(10)])
    emailtoken = ''
    for i in range(40):
        emailtoken += random.choice(allchar)
    
    url = domain + emailtoken
    return (url,emailtoken)


def Confirm(request,token):
    try:
        check = VerifyEmail.objects.get(token=token)
        status = 'found'
        check.approved = True
        check.save()
        context = {'status':status,'username':check.user.username, 'name':check.user.first_name}
    except:
        status = 'notfound'
        context = {'status':status}
    return render(request,'myapp/confirm.html',context)



#ส่ง Email
#------------------------------------------------------------


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
def EmailConfirm(email,name,token):
	subject = 'ยืนยันการสมัคร Suksan Fruit'
	newmember_name = name
	content = '''เนื่องจากความของการเข้าใช้ กรุณายืนยันอีเมล ผ่านลิงค์ล่างนี้'''

	link = token
	msg = 'สวัสดีคุณ {} \n\n {}\n Verify Link: {}'.format(newmember_name,content,link)
	sendthai(email,subject,msg)

#sendthai('moon0010010010@gmail.com',subject,msg)



#-------------------------------------------------------------


# HttpResponse คือ ฟังก์ชั่นสำหรับให้โชว์ข้อความหน้าเว็บได้

def Home(request):
	product = Allproduct.objects.all().order_by('id').reverse()[:3] #ดึงข้อมูลมาทั้งหมด
	preorder = Allproduct.objects.filter(quantity__lte=0) #quantity show product in stock 
	#quantity__lte=0 (หาค่าที่ quantity <= 0 - lte is <=) (underscore 2 ตัว)
	#quantity__gt=0 (หาค่าที่ quantity > 0 - gt is >)
	#quantity__gte=5 (หาค่าที่ quantity >= 5 - gte is >=)

	#product.reverse() #สลับลำดับ
	context = {'product':product, 'preorder': preorder}
	return render(request, 'myapp/home.html',context)
	#return HttpResponse()
	

def About(request):
	return render(request, 'myapp/about.html')

def Contact(request):
	return render(request, 'myapp/contact.html')

def Apple(request):
	return render(request, 'myapp/apple.html')


#ดึงข้อมูลจาก addproduct.html
#upload image
def AddProduct(request):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')

	if request.method == 'POST' and request.FILES['imageupload']:
		data = request.POST.copy()
		name = data.get('name')
		price = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')
		quantity = data.get('quantity')
		unit = data.get('unit')

		new = Allproduct()
		new.name = name
		new.price = price
		new.detail = detail
		new.imageurl = imageurl
		new.quantity = quantity
		new.unit = unit

		#---------------------Save Image----------------

		file_image = request.FILES['imageupload']
		file_image_name = request.FILES['imageupload'].name.replace(' ','')
		print('FILE_IMAGE:',file_image)
		print('IMAGE_NAME:',file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name,file_image)
		upload_file_url = fs.url(filename)
		new.image = upload_file_url[6:]

		#----------------------------------------------
		new.save()

	return render(request, 'myapp/addproduct.html')

def Product(request):
	product = Allproduct.objects.all().order_by('id').reverse() #ดึงข้อมูลมาทั้งหมด
	paginator = Paginator(product,2) # 1 หน้า show 3 ชิ้นเท่านั้น
	page = request.GET.get('page')
	product = paginator.get_page(page)
	#product.reverse() #สลับลำดับ
	context = {'product':product}
	return render(request, 'myapp/allproduct.html', context)


def Register(request):

	if request.method == 'POST':
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')

		#ยังไม่ใส่ try except เพื่อป้องกันไม่ให้การสมัครซ้ำ
		#alert ไปหน้าสมัครว่าอีเมลนี้เคยสมัครแล้ว

		newuser = User()
		newuser.username = email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name = last_name
		newuser.set_password(password)
		newuser.save()

		profile = Profile()
		profile.user = User.objects.get(username=email)
		profile.save()

		#-------------- Send Email Verify -----------------
		token,token_code = GenerateToken()
		EmailConfirm(email,first_name,token)
		getuser = User.objects.get(username=email)
		addverify = VerifyEmail()
		addverify.user = getuser
		addverify.token = token_code
		addverify.save()
		
		#sendthai(email,subject,msg)

		user = authenticate(username=email, password=password)
		login(request, user)

	return render(request, 'myapp/register.html')

def AddtoCart(request, pid):
	# localhost:8000/addtocart/id
	# {% url 'addtocart-page' pd.id %}
	print(request.user)
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid)

	try:
		#กรณีที่อัพเดทสืนค้าซ้ำกัน
		newcart = Cart.objects.get(user=user, productid=str(pid))
		#print('EXITS: ', pcheck.exists())
		newquan = newcart.quantity + 1
		newcart.quantity = newquan
		calculate = newcart.price * newquan
		newcart.total = calculate
		newcart.save()

		# update จำนวนของตะกร้าสินค้า ณ ตอนนี้
		count = Cart.objects.filter(user=user) #เช็คสินค้ามีเยอะแค่ไหน
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquantity = count
		updatequan.save()

		return redirect('allproduct-page')
	except:
		#สร้างสินค้าใหม่
		newcart = Cart()
		newcart.user = user
		newcart.productid = pid
		newcart.productname = check.name
		newcart.price = int(check.price)
		newcart.quantity = 1
		calculate = int(check.price) * 1
		newcart.total = calculate
		newcart.save()

		# update จำนวนของตะกร้าสินค้า ณ ตอนนี้
		count = Cart.objects.filter(user=user) #เช็คสินค้ามีเยอะแค่ไหน
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquantity = count
		updatequan.save()

		return redirect('allproduct-page')


def MyCart(request):
	username = request.user.username
	user = User.objects.get(username=username)

	context = {}

	if request.method == 'POST':
		#ใช้สำหรับการลบเท่านั้น
		data = request.POST.copy()
		productid = data.get('productid') #รับมาจาก mycart.html
		item = Cart.objects.get(user=user,productid=productid)
		item.delete()
		context['status'] = 'delete'

		#update number input cart
		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquantity = count
		updatequan.save()

	mycart = Cart.objects.filter(user=user)
	count = sum([ c.quantity for c in mycart])
	total = sum([ c.total for c in mycart])

		

	context['mycart'] =  mycart
	context['count'] = count
	context['total'] = total

	return render(request, 'myapp/mycart.html',context)




def MyCartEdit(request):
	#check user
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}

	if request.method == 'POST':
		#copy all submit
		data = request.POST.copy()

		if data.get('clear') == 'clear':
			clear = Cart.objects.filter(user=user).delete()
			#update all delete
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquantity = 0
			updatequan.save()
			return redirect('mycart-page')

		#create list for keep product
		editlist = []
		for k,v in data.items(): #get key and value
			#print([k,v])
			#pv_7
			if k[:2] == 'pd': #get pd input name from mycartedit.html
				pid = int(k.split('_')[1]) #cut words with _ underscore
				dt = [pid,int(v)] #new number
				editlist.append(dt)
		#print('Editlist: ',editlist)

		for ed in editlist:
			edit = Cart.objects.get(productid=ed[0],user=user) #productid, user
			edit.quantity = ed[1] # quantity
			calculate = edit.price * ed[1]
			edit.total = calculate
			edit.save()

		# update จำนวนสินค้าในตะกร้าสินตัวสีแดง ณ ตอนนี้
		count = Cart.objects.filter(user=user) #เช็คสินค้ามีเยอะแค่ไหน
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquantity = count
		updatequan.save()

		return redirect('mycart-page')
			
		#if data.get('checksave') == 'checksave':
		#return redirect('mycart-page')

		
	mycart = Cart.objects.filter(user=user)

	context['mycart'] =  mycart
	return render(request, 'myapp/mycartedit.html',context)


def Checkout(request):
	username = request.user.username
	user = User.objects.get(username=username)
	if request.method == 'POST':
		#รับค่าจาก html
		data = request.POST.copy()
		name = data.get('name')
		tel = data.get('tel')
		address = data.get('address')
		shipping = data.get('shipping')
		payment = data.get('payment')
		other = data.get('other')
		page = data.get('page')
		
		if page == 'information':
			context = {}
			context['name'] = name
			context['tel'] = tel
			context['address'] = address
			context['shipping'] = shipping
			context['payment'] = payment
			context['other'] = other

			mycart = Cart.objects.filter(user=user)
			count = sum([ c.quantity for c in mycart])
			total = sum([ c.total for c in mycart])

			context['mycart'] = mycart
			context['count'] = count
			context['total'] = total

			return render(request, 'myapp/checkout2.html',context)

		if page == 'confirm':
			print('Confirm')
			print(data)

			mycart = Cart.objects.filter(user=user)
			# id = OD-0007 2021 11 26 22 00 30
			# id = OD-00320200903220030
			mid = str(user.id).zfill(4)
			dt = datetime.now().strftime('%Y%m%d%H%M%S')
			orderid = 'OD' + mid + dt

			productorder = ''
			producttotal = 0
			
			for pd in mycart:
				order = OrderList()
				order.orderid = orderid
				order.productid = pd.productid
				order.productname = pd.productname
				order.price = pd.price
				order.quantity = pd.quantity
				order.total = pd.total
				order.save()

				#ส่งเข้าไปใน line
				productorder = productorder + 'ชื่อรายการ {}\n'.format(pd.productname) #รายการสินค้า
				producttotal += pd.total

			#Send to Line Notify in Group
			texttoline = 'คุณ ({})\n{}\n-------------------------\n{} ยอดรวม: {:,.2f} บาท \n ที่อยู่: {}\n เบอร์โทร: {}\n'.format(name,orderid,productorder,producttotal,address,tel)
			
			#หากสินค้ามากกว่า 10000 show sticker
			if producttotal > 100000:
				messenger.sticker(14,1,texttoline)
			else:
				messenger.sendtext(texttoline)

			#create order pedding
			odp = OrderPending()
			odp.orderid = orderid
			odp.user = user
			odp.name = name
			odp.tel = tel
			odp.address = address
			odp.shipping = shipping
			odp.payment = payment
			odp.other = other
			odp.save()


			#clear cart
			Cart.objects.filter(user=user).delete()
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquantity = 0
			updatequan.save()
			return redirect('mycart-page')

			# generate order Number and Save to OrderModels.
			# save Product in Cart to Order Product models.
			# clear Cart
			# redirect to Order list page

	return render(request, 'myapp/checkout1.html')


def OrderListPage(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}
	
	order = OrderPending.objects.filter(user=user)

	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)

		'''
			-

		'''
		

		total = sum([ c.total for c in odlist])
		od.total = total
		#สั่งนับว่า order นี้มีจำนวนกี่ชิ้น
		count = sum([ c.quantity for c in odlist])

	
		if od.shipping == 'ems':
			shipcost = sum([ 20 if i == 0 else 5 for i in range(count)])
			#shipcost = รวมค่าทั้งหมด (หากเป็นชิ้นแรกค่าจัดส่งจะคิด 20 บาท ชื้นถัดไปชิ้น 5 บาท)
		else:
			shipcost = sum([ 10 if i == 0 else 5 for i in range(count)])
		
		if od.payment == 'cod':
			shipcost += 10 #เก็บเงินปลายทาง
		od.shipcost = shipcost

	
	context['allorder'] = order



	return render(request, 'myapp/orderlist.html',context)




def AllOrderListPage(request):

	context = {}
	order = OrderPending.objects.all()

	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)
		total = sum([ c.total for c in odlist])
		od.total = total

		count = sum([ c.quantity for c in odlist])
		if od.shipping == 'ems':
			shipcost = sum([ 20 if i == 0 else 5 for i in range(count)])
		else:
			shipcost = sum([ 30 if i == 0 else 10 for i in range(count)])

		if od.payment == 'cod':
			shipcost += 20 #shipcost = shipcost + 20
		od.shipcost = shipcost

	paginator = Paginator(order,2)
	page = request.GET.get('page')
	order = paginator.get_page(page)
	context['allorder'] = order
	return render(request, 'myapp/allorderlist.html', context)





def UploadSlip(request,orderid):
	print('Order ID:', orderid)

	if request.method == 'POST' and request.FILES['slip']:
		data = request.POST.copy()
		sliptime = data.get('sliptime')
		
		update = OrderPending.objects.get(orderid=orderid)
		update.sliptime = sliptime
		
		file_image = request.FILES['slip']
		file_image_name = request.FILES['slip'].name.replace(' ','')
		print('FILE_IMAGE:', file_image)
		print('FILES_NAME:', file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name,file_image)
		upload_file_url = fs.url(filename)
		update.slip = upload_file_url[6:]
		update.save()


	odlist = OrderList.objects.filter(orderid=orderid)
	total = sum([ c.total for c in odlist])
	oddetail = OrderPending.objects.get(orderid=orderid)
	#คำนวณค่าส่งตามประเภทการส่ง
	count = sum([ c.quantity for c in odlist])
	if oddetail.shipping == 'ems': 
		shipcost = sum([ 20 if i == 0 else 1 for i in range(count)])
	else:
		shipcost = sum([ 10 if i == 0 else 1 for i in range(count)])
	
	if oddetail.payment == 'cod':
		shipcost += 10 # shipcost = shipcost + 20
	
	context = {'orderid':orderid, 
			   'total':total, 
			   'shipcost':shipcost,
			   'grandtotal':total+shipcost,
			   'oddetail':oddetail,
			   'count':count}

	#shipcost = รวมค่าทั้งหมด (หากเป้นชิ้นแรกค่าส่งจะคิด 50 บาท ชิ้นถัดไป 10 บาท)

	return render(request, 'myapp/uploadslip.html',context)


def UpdatePaid(request,orderid,status):

	if request.user.profile.usertype != 'admin':
		return redirect('home-page')

	order = OrderPending.objects.get(orderid=orderid)

	if status == 'confirm':
		order.paid = True
	elif status == 'cancel':
		order.paid = False
	order.save()
	return redirect('allorderlist-page')


def UpdateTracking(request,orderid):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')

	if request.method == 'POST':
		order = OrderPending.objects.get(orderid=orderid)
		data = request.POST.copy()
		trackingnumber = data.get('trackingnumber')
		order.trackingnumber = trackingnumber
		order.save()
		return redirect('allorderlist-page')

	order = OrderPending.objects.get(orderid=orderid)
	odlist = OrderList.objects.filter(orderid=orderid)

	total = sum([ c.total for c in odlist])
	order.total = total

	count = sum([ c.quantity for c in odlist])

	if order.shipping == 'ems':
		shipcost = sum([ 20 if i == 0 else 1 for i in range(count)])
	else:
		shipcost = sum([ 10 if i == 0 else 1 for i in range(count)])

	if order.payment == 'cod':
		shipcost += 10
	order.shipcost = shipcost

	context = {'orderid':orderid, 'order':order, 'odlist':odlist, 'total':total, 'count':count}

	return render(request, 'myapp/updatetracking.html',context)


def MyOrder(request,orderid):
	username = request.user.username
	user = User.objects.get(username=username)


	order = OrderPending.objects.get(orderid=orderid)
	#เช็คว่าเป็นของตัวเองไหม
	if user != order.user:
		return redirect('allproduct-page')

	odlist = OrderList.objects.filter(orderid=orderid)
	# shipcost calculate
	total = sum([ c.total for c in odlist])
	order.total = total

	count = sum([ c.quantity for c in odlist])

	if order.shipping == 'ems':
		shipcost = sum([ 20 if i == 0 else 1 for i in range(count)])
	else:
		shipcost = sum([ 10 if i == 0 else 1 for i in range(count)])

	if order.payment == 'cod':
		shipcost += 20
	order.shipcost = shipcost
	
	context = {'order':order,'odlist':odlist,'total':total,'count':count}


	return render(request, 'myapp/myorder.html',context)
