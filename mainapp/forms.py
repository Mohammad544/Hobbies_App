from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
	firstName = forms.CharField(max_length=20, required=False)
	lastName = forms.CharField(max_length=20, required=False)
	email = forms.EmailField()
	dob = forms.DateField(widget=forms.DateInput(format=["%d/%m/%Y"], attrs={"type": "date"}))
	city = forms.CharField(max_length=30)

	class Meta:
		model = User
		fields = ("username", "firstName", "lastName", "email", "password1", "password2", "dob", "city")

	