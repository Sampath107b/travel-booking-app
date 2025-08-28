from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import TravelOption, Booking, UserProfile
from datetime import datetime, timedelta

class TravelBookingTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client = Client()
        
        # Create user profile
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone_number='1234567890',
            address='Test Address'
        )
        
        # Create travel option
        self.travel_option = TravelOption.objects.create(
            type='FLIGHT',
            source='New York',
            destination='London',
            date_time=datetime.now() + timedelta(days=7),
            price=500.00,
            available_seats=100
        )

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
            'phone_number': '9876543210',
            'address': 'New User Address'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='newuser').exists())

    def test_travel_list_view(self):
        response = self.client.get(reverse('travel_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New York')
        self.assertContains(response, 'London')

    def test_booking_creation(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('book_travel', args=[self.travel_option.travel_id]), {
            'number_of_seats': 2
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful booking
        self.assertTrue(Booking.objects.filter(user=self.user, travel_option=self.travel_option).exists())
        
        # Check if available seats were updated
        updated_travel_option = TravelOption.objects.get(travel_id=self.travel_option.travel_id)
        self.assertEqual(updated_travel_option.available_seats, 98)

    def test_booking_cancellation(self):
        self.client.login(username='testuser', password='testpass123')
        # Create a booking
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2,
            total_price=1000.00,
            status='CONFIRMED'
        )
        
        response = self.client.post(reverse('cancel_booking', args=[booking.booking_id]))
        self.assertEqual(response.status_code, 302)  # Redirect after cancellation
        
        # Check if booking status was updated
        updated_booking = Booking.objects.get(booking_id=booking.booking_id)
        self.assertEqual(updated_booking.status, 'CANCELLED')
        
        # Check if seats were returned to travel option
        updated_travel_option = TravelOption.objects.get(travel_id=self.travel_option.travel_id)
        self.assertEqual(updated_travel_option.available_seats, 100)
