from django.contrib import admin
from django.urls import path
from mainapp.api import other_user_hobbies, get_user_data, update_user_image,update_user_details, get_user_hobbies, get_all_hobbies, create_new_hobby, add_hobby_user, get_friends, send_req, get_reqs, respond_req, remove_user_hobby, filter_users
from mainapp.views import related_hobbies, signup, profile
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
        path("", auth_views.LoginView.as_view(template_name="mainapp/login.html", redirect_authenticated_user=True), name="home"),
	path("api/related_users", other_user_hobbies, name ="other_user_hobbies"),
	path("related_hobbies", related_hobbies, name="related_hobbies"),
	path("login", auth_views.LoginView.as_view(template_name="mainapp/login.html", redirect_authenticated_user=True), name="login"),
	path("logout", auth_views.LogoutView.as_view(), name="logout"),
	path("signup", signup, name="signup"),
	path("profile", profile, name="profile"),
	path("api/get_user_data", get_user_data, name="get_user_data"),
	path("api/update_user_image", update_user_image, name="update_user_image"),
	path("api/update_user_details", update_user_details, name="update_user_details"),
	path("api/get_user_hobbies", get_user_hobbies, name="get_user_hobbies"),
	path("api/get_all_hobbies", get_all_hobbies, name="get_all_hobbies"),
	path("api/create_new_hobby", create_new_hobby, name="create_new_hobby"),
	path("api/add_hobby_user", add_hobby_user, name="add_hobby_user"),
	path("api/get_friends", get_friends, name="get_friends"),
	path("api/send_req", send_req, name="send_req"),
	path("api/get_reqs", get_reqs, name="get_reqs"),
	path("api/respond_req", respond_req, name="respond_req"),
	path("api/remove_user_hobby", remove_user_hobby, name="remove_user_hobby"),
	path("api/filter_users", filter_users, name="filter_users")
	
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


