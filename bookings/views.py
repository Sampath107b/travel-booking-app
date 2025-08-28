from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db import transaction
from .models import TravelOption, Booking, UserProfile
from .forms import UserRegistrationForm, UserProfileForm, BookingForm
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                # Create empty profile
                UserProfile.objects.create(user=user)
                login(request, user)
                messages.success(request, 'Registration successful! Please complete your profile.')
                return redirect('profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'bookings/register.html', {
        'form': form
    })

@login_required
def profile(request):
    # Get or create the user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        
    return render(request, 'bookings/profile.html', {
        'profile_form': profile_form
    })

def travel_list(request):
    travel_options = TravelOption.objects.filter(available_seats__gt=0)
    
    # Filter parameters
    travel_type = request.GET.get('type')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    date = request.GET.get('date')
    
    if travel_type:
        travel_options = travel_options.filter(type=travel_type)
    if source:
        travel_options = travel_options.filter(source__icontains=source)
    if destination:
        travel_options = travel_options.filter(destination__icontains=destination)
    if date:
        travel_options = travel_options.filter(date_time__date=date)
        
    return render(request, 'bookings/travel_list.html', {
        'travel_options': travel_options
    })

@login_required
def book_travel(request, travel_id):
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=travel_option)
        if form.is_valid():
            with transaction.atomic():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.travel_option = travel_option
                booking.total_price = travel_option.price * form.cleaned_data['number_of_seats']
                
                # Update available seats
                travel_option.available_seats -= form.cleaned_data['number_of_seats']
                if travel_option.available_seats < 0:
                    messages.error(request, 'Sorry, these seats are no longer available.')
                    return redirect('travel_list')
                    
                travel_option.save()
                booking.save()
                
                messages.success(request, 'Booking confirmed successfully!')
                return redirect('my_bookings')
    else:
        form = BookingForm(travel_option=travel_option)
        
    return render(request, 'bookings/book_travel.html', {
        'form': form,
        'travel_option': travel_option
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookings/my_bookings.html', {
        'bookings': bookings
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    if booking.status == 'CONFIRMED':
        with transaction.atomic():
            # Return seats to travel option
            travel_option = booking.travel_option
            travel_option.available_seats += booking.number_of_seats
            travel_option.save()
            
            booking.status = 'CANCELLED'
            booking.save()
            messages.success(request, 'Booking cancelled successfully!')
    
    return redirect('my_bookings')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')
