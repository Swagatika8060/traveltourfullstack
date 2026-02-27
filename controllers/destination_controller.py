from flask import Blueprint, render_template, request
from models.destination import Destination

destination_bp = Blueprint('destination', __name__)

@destination_bp.route('/destinations')
def destinations():
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'name')

    destinations = Destination.get_all(search, sort)

    return render_template('destinations.html',
                           destinations=destinations,
                           search=search,
                           sort=sort)
