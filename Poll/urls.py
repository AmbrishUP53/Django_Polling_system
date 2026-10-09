from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/' , views.login_view , name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('poll/<int:poll_id>/vote/', views.vote, name='vote'),
    path('poll/<int:poll_id>/results/', views.results, name='results'),
]