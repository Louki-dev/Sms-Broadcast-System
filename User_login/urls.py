from django.urls import path
from User_login.views import register_request, login_request, logout_request, user_profile, password_change

urlpatterns = [
    path('new/admin-register/', register_request, name='register'),
    path('admin-login/', login_request, name='login'),
    path('admin-logout/', logout_request, name='logout'),
    path('admin-edit_profile/', user_profile.as_view(), name='edit_profile'),
    path('admin-change_password/', password_change.as_view(), name="change_password"),
]


