from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path("study/", views.learning, name="study"),
    path('tests/', views.tests, name='tests'),
    path('about/', views.about, name='about'),
    path('lesson/<int:id>/', views.lesson_detail, name='lesson_detail'),
    path('test/<int:id>/', views.test_detail, name='test_detail'),
    # path('study/', views.study, name='study'),
    # path('tests/', views.tests, name='tests'),

]
