

from flask import Flask, render_template, request, url_for, redirect, flash,session
from controllers.admin_controller import admin_bp
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================
# MODELS
# ======================

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100))


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(255), nullable=False)
    package = db.Column(db.String(50), nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

# ======================
# FRONTEND ROUTES
# ======================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/destination')
def destination():
    destinations = Destination.query.all()
    return render_template('destination.html', destinations=destinations)

@app.route('/booking')
def booking():
    destinations = Destination.query.all()
    return render_template('booking.html', destinations=destinations)




# ======================
# SAVE BOOKING (AJAX)
# ======================

@app.route('/booking/save', methods=['POST'])
def save_booking():
    booking = Booking(
        name=request.form['name'],
        destination=request.form['destination'],
        contact=request.form['contact'],
        package=request.form['package'],
        adults=int(request.form['adults']),
        children=int(request.form['children']),
        date=request.form['date'],
        total_price=int(request.form['total_price'])
    )


    db.session.add(booking)
    db.session.commit()
    return "Saved", 200

# ======================
# HISTORY
# ======================

@app.route('/history')
def history():
    bookings = Booking.query.order_by(Booking.id.desc()).all()
    return render_template('history.html', bookings=bookings)

# ======================
# ADMIN DASHBOARD
# ======================

@app.route('/admin/dashboard')
def admin_dashboard():
    total_dest = Destination.query.count()
    total_bookings = Booking.query.count()
    return render_template(
        'admin_dashboard.html',
        total_dest=total_dest,
        total_bookings=total_bookings
    )

# ADMIN DESTINATION LIST + ADD
@app.route("/admin/destination", methods=["GET", "POST"])
def admin_destination():
    if request.method == "POST":
        name = request.form["name"]
        state = request.form["state"]
        description = request.form["description"]
        contact = request.form["contact"]
        price = int(request.form["price"])
        image = request.form["image"]

        dest = Destination(
            name=name,
            state=state,
            description=description,
            contact=contact,
            price=price,
            image=image
        )
        db.session.add(dest)
        db.session.commit()

        return redirect(url_for("admin_destination"))

    destinations = Destination.query.all()
    return render_template("admin_destination.html", destinations=destinations)

#   <edit destination>


@app.route("/admin/destination/edit/<int:id>", methods=["GET", "POST"])
def edit_destination(id):
    destination = Destination.query.get_or_404(id)

    if request.method == "POST":
        destination.name = request.form["name"]
        destination.state = request.form["state"]
        
        destination.description = request.form["description"]

        destination.contact = request.form["contact"]
        destination.price = int(request.form["price"])
        destination.image = request.form["image"]

        db.session.commit()
        return redirect(url_for("admin_destination"))

    return render_template("edit_destination.html", destination=destination)

@app.route("/admin/destination/delete/<int:id>", methods=["POST"])
def delete_destination(id):
    dest = Destination.query.get_or_404(id)
    db.session.delete(dest)
    db.session.commit()
    return redirect(url_for("admin_destination"))


# ADMIN BOOKING

@app.route('/admin/booking')
def admin_booking():
    bookings = Booking.query.all()
    return render_template('admin_booking.html', bookings=bookings)

@app.route('/admin/booking/delete/<int:id>', methods=['POST'])
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for('admin_booking'))



@app.route('/admin/booking/edit/<int:id>', methods=['GET', 'POST'])
def edit_booking(id):
    booking = Booking.query.get_or_404(id)
    destinations = Destination.query.all()

    if request.method == 'POST':
        booking.name = request.form['name']
        booking.destination = request.form['destination']
        booking.contact = request.form['contact']
        booking.package = request.form['package']
        booking.adults = int(request.form['adults'])
        booking.children = int(request.form['children'])
        booking.date = request.form['date']

        # 🔥 AUTO RECALCULATE PRICE
        destination = Destination.query.filter_by(
            name=booking.destination
        ).first()

        if destination:
            booking.total_price = (
                booking.adults * destination.price +
                booking.children * (destination.price // 2)
            )

        db.session.commit()
        flash("Booking updated successfully", "success")
        return redirect(url_for('admin_booking'))

    return render_template(
        'edit_booking.html',
        booking=booking,
        destinations=destinations
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

