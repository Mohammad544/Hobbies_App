from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
	"""
		The custome user model, from learn outs the user class should have
		profile image, email, city, date of birth, and a list of hobbies
		The default user already has email field so only fields needed are city,dob,hobbies,profile image

	"""
	city = models.CharField(max_length=30)
	dob = models.DateField(blank=True, null=True)
	image = models.ImageField(default="default.jpg", upload_to="profile_pics")
	friends = models.ManyToManyField(settings.AUTH_USER_MODEL)




class Hobby(models.Model):
	"""

	Model for hobbies 

	"""

	name = models.CharField(max_length=150)
	description = models.TextField()
	dateCreated = models.DateField(auto_now_add=True)
	users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="hobbies")

	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"description": self.description,
		}


class Request(models.Model):
	sender = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, related_name="sender1",on_delete=models.CASCADE)
	reciver = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE) #reciever spelt incorrectly here and throughout files



