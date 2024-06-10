from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name="home_page"),
]