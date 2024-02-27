# Flight-Ticket-Booking
The objective of this project was to develop a web application for flight ticket booking, catering to two types of users - regular users and administrators. The application provides functionalities like user authentication, flight search, ticket booking, viewing bookings, and flight management for admins.

# Running the Flight Ticket Booking Web Application: 
**(Default Admin Username: Admin, Default Admin Password: 123456)**
To run the Flight Ticket Booking Web Application, follow these steps:
1. Install Required Libraries:
Ensure that you have Python installed on your system. Install the required libraries using the following command:
``pip install Flask Flask-Login pymongo`` or  ``pip install -r requirements.txt``

2. Database Setup:
MongoDB should be installed and running on your machine.
Create a database named "flight_booking" and collections named "users", "flights", and "bookings".

3. Run the Application:
Open a terminal and navigate to the project directory.
Run the Flask application using the command:
``python app.py``

# Tech Stack Used:
- Frontend:
HTML
CSS
Jinja2 (templating engine for Flask)

- Backend:
Python
Flask (web framework)
MongoDB (database for storing user information, flight details, and bookings)

- Authentication: Flask-Login for user authentication

- Data Modeling: MongoDB collections for users, flights, and bookings

- Version Control: Git for source code management

- Deployment: I also know deployment of basic Python Applications and have a basic idea of AWS deployment.

# User Functionalities:
- Login/Signup: Users can create accounts or log in with existing credentials.
- Flight Search: Users can search for flights based on date and time.
- Booking Tickets: Users can book tickets on a flight based on availability.
- My Bookings: Users can view all their bookings in one place.
- Logout: Users can log out securely.

# Admin Functionalities:
- Admin Login: Admins have a separate login to access admin functionalities.
- Add Flights: Admins can add new flights with details like name, source, destination, fare, flight number, time, and seats.
- Remove Flights: Admins can remove existing flights from the system.
- View All Bookings: Admins can view all the bookings based on flight number and time.

# Challenges Faced:

- User Authentication: Implementing secure user authentication using Flask-Login.
- MongoDB Integration: Setting up the MongoDB database and integrating it with Flask.
- Querying and updating documents based on user and admin actions.
- Frontend Design: Creating a simple yet user-friendly UI using HTML and CSS.
- Implementing Jinja2 templates to dynamically display data.
- Complexity: The complexity of this project lies in managing user sessions, secure authentication, and database interactions. Implementing the logic for flight bookings, ensuring data consistency, and -displaying relevant information to users and admins were key challenges.


# Future Improvements:

- Enhanced UI: Implementing a more polished and responsive user interface.
- Payment Integration: Adding payment gateways for real transactions.
- User and Admin Dashboards: Creating dedicated dashboards for users and admins with more functionalities.
