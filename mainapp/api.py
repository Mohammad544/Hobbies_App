from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from .models import User, Hobby, Request
from django.contrib.auth.decorators import login_required
import json
from datetime import date

@login_required
def other_user_hobbies(request):
	"""
	This creates a dictionary and stores the number of similar hobbies between the current user
	and every other user in the database. The sorted dictionary is returned to the client.
	
	"""
	if request.method == "GET":
		currentUser = request.user
		allUsers = User.objects.all()
		thisHobbies = currentUser.hobbies.all()
		realtional = {}
		for i in allUsers:
			if i.username == currentUser.username or i.username == "admin":
				continue
			today = date.today()
			birthdate=i.dob
			age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
			realtional[i.username] = {
				"inCommon" : 0,
				"age": age,
				"city": i.city.lower()
			}
			tmpHobbies = i.hobbies.all()
			for x in tmpHobbies:
				if x in thisHobbies:
					realtional[i.username]["inCommon"] += 1

		final = {k:v for k,v in sorted(realtional.items(), reverse= True, key=lambda y: y[1]["inCommon"])} #Sort the dictionary in descending order		
		return JsonResponse(final)
	
	return HttpResponseBadRequest("error")


@login_required
def get_user_data(request):
	if request.method == "GET":
		currentuser = request.user
		imgurl = currentuser.image.url
		email = currentuser.email
		city = currentuser.city
		dob = currentuser.dob
		print(city)
		return JsonResponse({
			"imgurl": imgurl,
			"email" : email,
			"city" : city,
			"dob" : dob
			})


@login_required
def update_user_image(request):
	if request.method == "POST":
		image = request.FILES["file"]
		currentuser = request.user
		currentuser.image = image
		currentuser.save()
		return JsonResponse({})
	return HttpResponseBadRequest("error")


@login_required
def update_user_details(request):
	if request.method == "PUT":
		currentuser = request.user
		data = json.loads(request.body)
		if data["field"] == "email":
			currentuser.email = data["new"]
		elif data["field"] == "dob":
			currentuser.dob	= data["new"]
		elif data["field"] == "city":
			currentuser.city = data["new"]
		currentuser.save()
		return JsonResponse({})
	return HttpResponseBadRequest("error")


@login_required
def get_user_hobbies(request):
	if request.method == "GET":
		currentuser =request.user
		return JsonResponse({
			"hobbies": [hobby.to_dict() for hobby in currentuser.hobbies.all()]
			})
	return HttpResponseBadRequest("error")

@login_required
def get_all_hobbies(request):
	if request.method == "GET":
		return JsonResponse({
				"hobbies" : [hobby.to_dict() for hobby in Hobby.objects.all()]

			})
	return HttpResponseBadRequest("error")


@login_required
def create_new_hobby(request):
	if request.method == "POST":
		data = json.loads(request.body)
		name = data["name"]
		description = data["description"]
		x = Hobby(name=name, description=description)
		x.save()
		return JsonResponse({})

	return HttpResponseBadRequest({})


@login_required
def add_hobby_user(request):
	if request.method == "PUT":
		data = json.loads(request.body)
		hobbyid = data["id"]
		currentuser = request.user
		toadd = Hobby.objects.get(id=hobbyid)
		currentuser.hobbies.add(toadd)
		currentuser.save()
		return JsonResponse({})
	return HttpResponseBadRequest("error")


@login_required
def get_friends(request):
	if request.method == "GET":
		currentuser = request.user
		x = currentuser.friends.all()

		return JsonResponse({
			"friends" : [i.username for i in x],
			})
	return HttpResponseBadRequest("error")


@login_required
def send_req(request):
	if request.method == "POST":
		currentuser = request.user
		data = json.loads(request.body)
		reciever = User.objects.get(username=data["username"])
		reqs = Request.objects.all()
		for i in reqs:
			if i.reciver == reciever and i.sender == currentuser:
				return JsonResponse({})
		newreq = Request(sender=currentuser,reciver=reciever)
		newreq.save()
		return JsonResponse({})
	return HttpResponseBadRequest("error")


@login_required
def get_reqs(request):
	if request.method == "GET":
		currentuser = request.user
		usernames = []
		for i in Request.objects.all():
			if i.reciver == currentuser:
				usernames.append(i.sender.username)

		return JsonResponse({
			"reqs" : usernames,
			})
	return HttpResponseBadRequest("error")


@login_required
def respond_req(request):
	if request.method == "DELETE":
		currentuser = request.user
		data = json.loads(request.body)
		choice = data["choice"]
		sender = User.objects.get(username=data["sender"])
		req = Request.objects.get(sender=sender, reciver=currentuser)
		if choice == "accept":
			print("accepted")
			currentuser.friends.add(sender)
			sender.friends.add(currentuser)
		req.delete()
		return JsonResponse({})
	return HttpResponseBadRequest("error")


@login_required
def remove_user_hobby(request):
	if request.method == "DELETE":
		currentuser = request.user
		data = json.loads(request.body)
		hobby = Hobby.objects.get(id = data["id"])
		currentuser.hobbies.remove(hobby)
		currentuser.save()
		return JsonResponse({})
	return HttpResponseBadRequest("error")


@login_required
def filter_users(request):
	if request.method == "POST":
		data= json.loads(request.body)
		city = data["city"]
		minage = data["min"]
		maxage = data["max"]
		if minage == "": 
			minage = None
		else: minage = int(minage)
		if maxage == "": 
			maxage = None
		else: maxage = int(maxage)
		if city == "": city = None
		x = data["data"]
		new = {}
		try:
			if city == None and maxage == None and minage == None:
				return JsonResponse(x)
			elif minage == None and city != None and maxage != None:
				for k,v in x.items():
					if not(x[k]["age"] > maxage or x[k]["city"].lower() != city.lower()):new[k] = v
			elif maxage == None and city != None and minage != None:
				for k,v in x.items():
					if not(x[k]["age"] < minage or x[k]["city"].lower() != city.lower()):new[k] = v
			elif city == None and maxage == None:
				for k,v in x.items():
					if not(x[k]["age"] < minage):new[k] = v
			elif minage == None and maxage == None:
				for k,v in x.items():
					if not(x[k]["city"].lower() != city.lower()):new[k] = v			
			elif city == None and minage == None:
				for k,v in x.items():
					if not(x[k]["age"] > maxage):new[k] = v
			elif city == None and minage != None and maxage != None:
				for k,v in x.items():
					if not(minage > x[k]["age"] or maxage < x[k]["age"]): new[k]= v
			elif city != None and minage != None and maxage != None:
				for k,v in x.items():
					if not(minage > x[k]["age"] or maxage < x[k]["age"] or x[k]["city"].lower() != city.lower()):
						new[k] = v
			return JsonResponse(new)
		except: #city doesnt exist
			return JsonResponse({}) 
	return HttpResponseBadRequest("error")


