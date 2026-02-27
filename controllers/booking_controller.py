
from flask import Blueprint, render_template, request, redirect, url_for
from models.booking import Booking
from models.destination import Destination

booking_bp = Blueprint('booking', __name__)

# BOOKING PAGE
@booking_bp.route('/booking', methods=['POST'])
def booking_page():
    destinations = Destination.get_all()
    return render_template('booking.html', destinations=destinations)

# SAVE BOOKING
@booking_bp.route('/booking', methods=['POST'])
def booking():
    package_days = {
        "Standard": 3,
        "Premium": 5,
        "Deluxe": 7
    }
    data = {
        "name": request.form['name'],
        "destination": request.form['destination'],
        "contact": request.form['contact'],
        "package": request.form['package'],
        "adults": int(request.form['adults']),
        "children": int(request.form['children']),
        "date": request.form['date'],
        "total_price": float(request.form['total_price'])
    }

    Booking.create(data)
    return redirect(url_for('history'))