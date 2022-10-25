from django.test import TestCase
from django.urls import reverse
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .models import User

# Create your tests here.
class SignUpTest(LiveServerTestCase):

	def testform(self):
		selenium = webdriver.Chrome()
		url = reverse("signup")
		selenium.get('%s%s' % (self.live_server_url, url))

		username = selenium.find_element_by_id('id_username')
		firstname = selenium.find_element_by_id('id_firstName')
		lastname = selenium.find_element_by_id('id_lastName')
		email = selenium.find_element_by_id('id_email')
		pass1 = selenium.find_element_by_id('id_password1')
		pass2 = selenium.find_element_by_id('id_password2')
		dob = selenium.find_element_by_id('id_dob')
		city = selenium.find_element_by_id('id_city')
		submit = selenium.find_element_by_css_selector("button[type='submit']")


		username.send_keys('selTester')
		firstname.send_keys('selenium')
		lastname.send_keys('testing')
		email.send_keys('test@email.com')
		pass1.send_keys('seleniumpassword')
		pass2.send_keys('seleniumpassword')
		dob.send_keys('23/12/2000')
		city.send_keys('London')
		
		submit.send_keys(Keys.RETURN)	
		assert "login" in selenium.page_source



class LoginTest(TestCase):
	def setUp(self):
		self.credentials = {
		"username" : "hamzah23",
		"password" : "hamzahpassword"
		}
		User.objects.create_user(**self.credentials)
	def test_login(self):
		response = self.client.post("/login", self.credentials, follow=True)
		self.assertTrue(response.context['user'].is_active)


