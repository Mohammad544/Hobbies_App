from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def related_hobbies(request):
	return render(request, "mainapp/related_hobbies.html")

def signup(request):
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("login")
	else:
		form = SignupForm()
	return render(request, "mainapp/signup.html", {"form" : form})

@login_required
def profile(request):
	return render(request, "mainapp/profile.html", context={"user": request.user})
