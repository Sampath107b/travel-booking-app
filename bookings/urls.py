from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

urlpatterns = [
    path('', views.travel_list, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='bookings/login.html',
        authentication_form=CustomLoginForm,
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('travel/', views.travel_list, name='travel_list'),
    path('book/<int:travel_id>/', views.book_travel, name='book_travel'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
