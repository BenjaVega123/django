from django.urls import path
from . import views
app_name = "users_app"

urlpatterns = [
    path('register/', views.UserRegisterCreateView.as_view(), name="register_user"),
    path('login/', views.LoginUser.as_view(), name="login_user"),
    path('logout/', views.LogoutView.as_view(), name="logout_user"),
    path('update/', views.UpdatePassword.as_view(), name="update_user"),

]
