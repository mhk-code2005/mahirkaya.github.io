from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path('research/', views.research, name='research'),
    path('resume/', views.resume, name='resume'),
    path('projects/', views.projects, name='projects'),
    path('bookrec/', views.bookrec, name='bookrec'),
    path('livescores/', views.livescores, name='livescores'),

]