from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField
from django.db.models.fields.files import ImageField

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	photo = models.ImageField(upload_to="photoprofile", null=True,blank=True,default='default.png')
	usertype = models.CharField(max_length=100,default='member')
	cartquantity = models.IntegerField(default=0)

	def __str__(self):
		return self.user.first_name


class Allproduct(models.Model):
	name = models.CharField(max_length=100)
	price = models.CharField(max_length=100)
	detail = models.TextField(null=True,blank=True)
	imageurl = models.CharField(max_length=200,null=True,blank=True)
	instock = models.BooleanField(default=True)
	quantity = models.IntegerField(default=1)
	unit = models.CharField(max_length=200,default='-')
	image = models.ImageField(upload_to="products",null=True,blank=True)


	def __str__(self):
		return self.name

class Cart(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	productid = models.CharField(max_length=100)
	productname = models.CharField(max_length=100)
	price = models.IntegerField()
	quantity = models.IntegerField()
	total = models.IntegerField()
	stamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)

class OrderList(models.Model):
	orderid = models.CharField(max_length=100)
	productid = models.CharField(max_length=100)
	productname = models.CharField(max_length=100)
	price = models.IntegerField()
	quantity = models.IntegerField()
	total = models.IntegerField()

class OrderPending(models.Model):
	orderid = models.CharField(max_length=100)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	tel = models.CharField(max_length=100)
	address = models.TextField()
	shipping = models.CharField(max_length=100)
	payment = models.CharField(max_length=100)
	other = models.TextField(null=True,blank=True)
	stamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	paid = models.BooleanField(default=False)
	slip = models.ImageField(upload_to="slip",null=True,blank=True)
	sliptime = models.CharField(max_length=100,null=True,blank=True) # datetime with calendar html
	paymentid = models.CharField(max_length=100,null=True,blank=True)
	trackingnumber = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.orderid


class VerifyEmail(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	token = models.CharField(max_length=100)
	approved = models.BooleanField(default=False)