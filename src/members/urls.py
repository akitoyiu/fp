from django.contrib import admin
from django.urls import path
from .views import RegisterView, EditProfileView, ChangePasswordView, password_success
from .views import ListProfileView, ShowProfileView, EditUserProfileView
from django.contrib.auth import views as auth_view
from django.conf.urls import url

urlpatterns = [

    path('register/', RegisterView.as_view(), name="register"),
    path('<int:uid>/edit_profile/', EditProfileView, name="edit_profile"),
    #path('list_profile/', ListProfileView.as_view(), name="list_profile"),
    url(r'^list_profile/$', ListProfileView.as_view(), name='list_profile'),  #Need to use this for pagination

    # Default Django Password Change View
    #path('password/', auth_view.PasswordChangeView.as_view(template_name='registration/change_password.html')),
    path('password/', ChangePasswordView.as_view(), name="changePassword"),

    path('password_changed/', password_success, name="password_success"),

    #User Profile page
    path('<int:pk>/profile/', ShowProfileView.as_view(), name="show_profile"),
    path('<int:pk>/edit_userprofile/', EditUserProfileView.as_view(), name="edit_userprofile"),

]
