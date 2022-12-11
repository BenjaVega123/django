from django.urls import path
from . import views
app_name = "home_app"

urlpatterns = [
    path('home/', views.HomePage.as_view(), name="home_page"),
    path('mixin/', views.PruebaMixin.as_view(), name="mixin"),
]
