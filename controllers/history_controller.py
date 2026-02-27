
from flask import Blueprint, render_template, request
from models.booking import Booking

history = Blueprint('history', __name__)

@history.route('/history')
def history():
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'id')

    query = Booking.query

    # SEARCH (only valid columns)
    if search:
        query = query.filter(
            (Booking.name.ilike(f"%{search}%")) |
            (Booking.destination.ilike(f"%{search}%"))
        )

    # SORT
    if sort == "date":
        query = query.order_by(Booking.date.desc())
    else:
        query = query.order_by(Booking.id.desc())

    bookings = query.all()

    return render_template(
        'history.html',
        bookings=bookings,
        search=search,
        sort=sort
    )
