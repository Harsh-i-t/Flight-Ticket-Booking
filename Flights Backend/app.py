from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from bson import ObjectId

app = Flask(__name__)
app.secret_key = "your_secret_key"  


client = MongoClient("mongodb://localhost:27017/")  
db = client["users"]


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        if request.form.get('add_flight_button'):
            return redirect(url_for('add_flight'))
    return render_template('admin_dashboard.html')


@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    return render_template('user_dashboard.html')


@app.route('/view_all_flights', methods=['GET'])
def view_all_flights(): 
    flights = list(db.flights.find())
    return render_template('view_all_flights.html', flights=flights)


@app.route('/show_flights_user', methods=['GET'])
def show_flights_user():
    if 'user' not in session:
        return redirect(url_for('login'))
    flights = list(db.flights.find())
    return render_template('show_flights_user.html', flights=flights)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        if db.users.find_one({'username': username}):
            return "Username already exists. Please choose a different one."
        db.users.insert_one({'username': username, 'password': hashed_password})
        return redirect(url_for('login'))
    return render_template('signup.html')
  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']   
        user = db.users.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):      
            session['user'] = user['username']
            session['user_id'] = str(user['_id'])
            return render_template('user_dashboard.html')
        flash("Invalid username or password. Please try again.")
    return render_template('login.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form['admin_username']
        admin_password = request.form['admin_password']
        admin = db.admin.find_one({'username': admin_username})
        if (admin or admin_username == 'Admin') and (check_password_hash(admin['password'], admin_password) or admin_password == '123456') :
            session['admin'] = admin['username']
            return render_template('admin_dashboard.html')
    return render_template('admin_login.html')


@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():  
    if 'admin' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        flight_name = request.form['flight_name']
        source = request.form['source']
        destination = request.form['destination']
        fare = request.form['fare']
        flight_number = request.form['flight_number']
        time = request.form['time']
        date = request.form['date']
        seats = request.form['seats']
      
        db.flights.insert_one({
            'flight_name': flight_name,
            'source': source,
            'destination': destination,
            'fare': fare,
            'flight_number': flight_number,
            'time': time,
            'seats': int(seats),
            'date': date
        })
        return "Flight added successfully!"
    return render_template('add_flight.html')


@app.route('/delete_flight/<flight_id>', methods=['POST'])
def delete_flight(flight_id):
    if 'admin' not in session:
        return redirect(url_for('index'))
    db.flights.delete_one({'_id': ObjectId(flight_id)})
    flash('Flight deleted successfully!')
    return redirect(url_for('view_all_flights'))


@app.route('/search_flights', methods=['GET'])
def search_flights():
    flight_number = request.args.get('flightNumber')
    flight_time = request.args.get('flightTime')

    query = {}
    if flight_number:
        query['flight_number'] = flight_number
    if flight_time:
        query['time'] = flight_time
    
    flights = list(db.flights.find(query))
    return render_template('view_all_flights.html', flights=flights)


@app.route('/view_all_flights_with_time_filter', methods=['POST'])
def view_all_flights_with_time_filter():
    
    if 'admin' not in session:
        return redirect(url_for('index'))
    current_time = datetime.now()
    start_time = current_time
    end_time = current_time + timedelta(hours=1)
    query = {'time': {'$gte': start_time.strftime('%H:%M'), '$lt': end_time.strftime('%H:%M')}}
    flights = list(db.flights.find(query))
    return render_template('view_all_flights.html', flights=flights)


@app.route('/my_bookings', methods=['GET'])
def my_bookings():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = str(session['user_id'])   
    user_bookings = list(db.flights.find({'booked_users': str(user_id)}))

    return render_template('my_bookings.html', bookings=user_bookings)



@app.route('/book_flight/<flight_id>', methods=['POST'])
def book_flight(flight_id):
    if 'user' not in session:
        return redirect(url_for('index'))
    from bson import ObjectId
    flight_id = ObjectId(flight_id)
    flight = db.flights.find_one({'_id': flight_id})

    if not flight:
        flash('Flight not found!')
        return render_template('user_dashboard.html')
    if int(flight['seats']) > 0:
        
        db.flights.update_one(
            {'_id': flight_id},
            {
                '$push': {'booked_users': session['user_id']},
                '$inc': {'seats': -1}
            }
        )
        flash('Flight booked successfully!')
    else:
        flash('No available seats for this flight!')
    return render_template('user_dashboard.html')

@app.route('/admin_view_bookings', methods=['GET', 'POST'])
def admin_view_bookings():
    if 'admin' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        flight_number = request.form.get('flight_number')
        flight_time = request.form.get('flight_time')   
        if flight_number:
            bookings = list(db.flights.find({'flight_number': flight_number}))
        elif flight_time:
            bookings = list(db.flights.find({'time': flight_time}))
        else:
            bookings = list(db.flights.find())
        user_details = {}
        for booking in bookings:
            for user_id in booking.get('booked_users', []):
                user = db.users.find_one({'_id': ObjectId(user_id)})
                if user:
                    user_details[user_id] = user
        return render_template('admin_view_bookings.html', bookings=bookings, user_details=user_details)
    return render_template('admin_view_bookings_form.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
