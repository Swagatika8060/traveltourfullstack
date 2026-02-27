

from flask import Blueprint, app, render_template, request, redirect, url_for, flash, session
from models.database import db
from models.user import User
from models.booking import Booking
from models.destination import Destination

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# =============================
# ADMIN LOGIN
# =============================
@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = User.query.filter_by(username=username, role="admin").first()

        if admin and admin.verify_password(password):
            session["admin_id"] = admin.id
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("admin/login.html")


# =============================
# ADMIN LOGOUT
# =============================
@admin_bp.route("/logout")
def admin_logout():
    session.pop("admin_id", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("admin.admin_login"))


# =============================
# ADMIN DASHBOARD
# =============================
@admin_bp.route("/dashboard")
def dashboard():
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    return render_template(
        "admin/dashboard.html",
        total_bookings=Booking.query.count(),
        total_destinations=Destination.query.count(),
        total_users=User.query.count()
    )


# =============================
# DESTINATION LIST
# =============================
@admin_bp.route("/destinations")
def destinations_list():
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    destinations = Destination.query.order_by(Destination.id.desc()).all()
    return render_template("admin/destinations.html", destinations=destinations)


# =============================
# ADD DESTINATION
# =============================



@admin_bp.route("/destination/add", methods=["GET", "POST"])
def destination_add():
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    if request.method == "POST":
        destination = Destination(
            name=request.form.get("name"),
            state=request.form.get("state"),
           
            description=request.form.get("description"),
            contact=request.form.get("contact"),
            image=request.form.get("image"),
            price=request.form.get("price"),
            days=request.form.get("days")
        )
        db.session.add(destination)
        db.session.commit()
        flash("Destination added successfully", "success")
        return redirect(url_for("admin.destinations_list"))

    return render_template("admin/destination_add.html")


# =============================
# EDIT DESTINATION
# =============================

@admin_bp.route("/destination/edit/<int:id>", methods=["GET", "POST"])
def edit_destination(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    destination = Destination.query.get_or_404(id)

    if request.method == "POST":
        destination.name = request.form.get("name")
        destination.state = request.form.get("state")
       
        destination.description = request.form.get("description")
        destination.contact = request.form.get("contact")
        destination.image = request.form.get("image")
        destination.price = int(request.form.get("price"))
        destination.days = request.form.get("days")

        db.session.commit()
        flash("Destination updated successfully", "success")
        return redirect(url_for("admin_destination"))

    return render_template("edit_destination.html", destination=destination)

# delete destination

@admin_bp.route("/destination/delete/<int:id>", methods=["POST"])
def delete_destination(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    destination = Destination.query.get_or_404(id)
    db.session.delete(destination)
    db.session.commit()
    flash("Destination deleted", "info")
    return redirect(url_for("admin_destination"))

# =============================
# BOOKINGS LIST (SEARCH + SORT)
# =============================
@admin_bp.route("/bookings")
def bookings_list():
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    search = request.args.get("search", "").strip()
    sort = request.args.get("sort", "latest")

    query = Booking.query.join(Destination)

    if search:
        query = query.filter(
            Booking.name.ilike(f"%{search}%") |
            Destination.name.ilike(f"%{search}%")
        )

    if sort == "latest":
        query = query.order_by(Booking.id.desc())
    elif sort == "oldest":
        query = query.order_by(Booking.id.asc())
    elif sort == "price_high":
        query = query.order_by(Booking.total_price.desc())
    elif sort == "price_low":
        query = query.order_by(Booking.total_price.asc())

    bookings = query.all()

    return render_template(
        "admin_booking.html",
        bookings=bookings,
        search=search,
        sort=sort
    )


# =============================
# EDIT BOOKING
# =============================

@admin_bp.route('/admin/booking/edit/<int:id>', methods=['GET', 'POST'])
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

        # ✅ PRICE RECALC (THIS WAS MISSING)
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

# =============================
# DELETE BOOKING
# =============================
@admin_bp.route("/booking/delete/<int:id>", methods=["POST"])
def booking_delete(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()

    flash("Booking deleted successfully", "info")
    return redirect(url_for("admin_booking"))