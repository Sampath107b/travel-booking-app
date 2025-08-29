# Travel Booking Application
🔗 Live: https://sampath107b.pythonanywhere.com
A Django-based web application for booking travel tickets (flights, trains, and buses).

## Features

- User registration and authentication
- Profile management
- Travel options listing with filtering
- Booking management
- Responsive design using Bootstrap
- MySQL database integration

## Requirements

- Python 3.11+
- MySQL Server
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd travel-booking-application
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a MySQL database:
```sql


```

5. Create a `.env` file in the project root and add your configurations:
```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=travel_booking
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=3306
```

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

1. Register a new user account or log in with existing credentials
2. Browse available travel options
3. Use filters to find specific travel options
4. Book tickets by selecting the number of seats
5. View and manage your bookings
6. Update your profile information

## Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin/` to:
- Manage travel options
- View and manage bookings
- Manage user profiles

## Testing

To run the tests:
```bash
python manage.py test
```

## Deployment

For production deployment:

1. Set DEBUG=False in .env
2. Configure your web server (e.g., Nginx, Apache)
3. Use a production-grade server like Gunicorn
4. Set up SSL certificates for HTTPS

## License

This project is licensed under the MIT License - see the LICENSE file for details.
