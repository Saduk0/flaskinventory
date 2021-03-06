from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.models import User, Product, Location, Movement
from flaskr import db

bp = Blueprint('inventory',__name__)

@bp.route('/')
def index():
    products = Product.query.all()
    locations = Location.query.all()
    movements = Movement.query.all()
    return render_template('inventory/index.html', products=products, locations=locations, movements=movements)

@bp.route('/createproduct', methods=('GET', 'POST'))
@login_required
def createproduct():
    if request.method == 'POST':
        productName = request.form['productName']
        # amount = request.form['amount']
        error = None

        if not productName:
            error = 'Product name is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (productName, author_id)'
                ' VALUES (?, ?)',
                (productName, g.user['id'])
            )
            db.commit()
            return redirect(url_for('inventory.index'))
    return render_template('inventory/createproduct.html')

def get_product(id, check_author=True):
    product = Product.query.get(id)
    if product is None:
        abort(404, "Product id {0} doesn't exist.".format(id))

    if check_author and product['author_id'] != g.user['id']:
        abort(403)

    return product

@bp.route('/<int:id>/updateproduct', methods=('GET', 'POST'))
@login_required
def updateproduct(id):
    product = get_product(id)

    if request.method =='POST':
        productName = request.form['productName']
        # amount = request.form['amount']
        error = None
        if not productName:
            error = 'Product Name is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE product SET productName = ?'
                ' WHERE id = ?',
                (productName, id)
            )
            db.commit()
            return redirect(url_for('inventory.index'))

    return render_template('inventory/updateproduct.html', product=product)

@bp.route('/<int:id>/deleteproduct', methods=('POST',))
@login_required
def deleteproduct(id):
    get_product(id)
    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('inventory.index'))

@bp.route('/p<int:id>/', methods=('GET',))
def viewproduct(id):
    product = get_product(id, check_author=False)

    return render_template('inventory/viewproduct.html', product=product)


###


@bp.route('/createlocation', methods=('GET', 'POST'))
@login_required
def createlocation():
    if request.method == 'POST':
        locationName = request.form['locationName']
        #amount = request.form['amount']
        error = None

        if not locationName:
            error = 'Location name is required.'
        # if not amount:
        #     error = 'Amount is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO location (locationName, author_id)'
                ' VALUES (?, ?)',
                (locationName, g.user['id'])
            )
            db.commit()
            return redirect(url_for('inventory.index'))
    return render_template('inventory/createlocation.html')

def get_location(id, check_author=True):
    location = get_db().execute(
        'SELECT p.id, locationName, created, author_id, username'
        ' FROM location p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    if location is None:
        abort(404, "Location id {0} doesn't exist.".format(id))

    if check_author and location['author_id'] != g.user['id']:
        abort(403)

    return location

@bp.route('/<int:id>/updatelocation', methods=('GET', 'POST'))
@login_required
def updatelocation(id):
    location = get_location(id)

    if request.method =='POST':
        locationName = request.form['locationName']
        # amount = request.form['amount']
        error = None
        if not locationName:
            error = 'Location Name is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE location SET locationName = ?'
                ' WHERE id = ?',
                (locationName, id)
            )
            db.commit()
            return redirect(url_for('inventory.index'))

    return render_template('inventory/updatelocation.html', location=location)

@bp.route('/<int:id>/deletelocation', methods=('POST',))
@login_required
def deletelocation(id):
    get_location(id)
    db = get_db()
    db.execute('DELETE FROM location WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('inventory.index'))

@bp.route('/l<int:id>/', methods=('GET',))
def viewlocation(id):
    location = get_location(id, check_author=False)

    return render_template('inventory/viewlocation.html', location=location)

####


@bp.route('/createmovement', methods=('GET', 'POST'))
@login_required
def createmovement():
    if request.method == 'POST':
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        product_id = request.form['product_id']
        qty = request.form['qty']

        error = None

        if not from_location or to_location:
            error = 'Location is required.'
        if not product_id:
            error = 'Product is required.'
        if not qty:
            error = 'Quantity is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO movements (from_location, to_location, product_id, qty, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (from_location, to_location, product_id, qty, g.user['id'])
            )
            db.commit()
            return redirect(url_for('inventory.index'))
    return render_template('inventory/createmovement.html')

def get_movement(id, check_author=True):
    movement = get_db().execute(
        'SELECT p.id, from_location, to_location, product_id, qty, created, author_id, username'
        ' FROM movements p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    if movement is None:
        abort(404, "movement id {0} doesn't exist.".format(id))

    if check_author and movement['author_id'] != g.user['id']:
        abort(403)

    return movement

@bp.route('/<int:id>/updatemovement', methods=('GET', 'POST'))
@login_required
def updatemovement(id):
    movement = get_movement(id)

    if request.method =='POST':
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        product_id = request.form['product_id']
        qty = request.form['qty']
        error = None
        if not from_location:
            error = 'Location is required.'
        if not product_id:
            error = 'Product is required.'
        if not qty:
            error = 'Quantity is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE movements SET (from_location, to_location, product_id, qty, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (from_location, to_location, product_id, qty, g.user['id'])
            )
            db.commit()
            return redirect(url_for('inventory.index'))

    return render_template('inventory/updatemovement.html', movement=movement)

@bp.route('/<int:id>/deletemovement', methods=('POST',))
@login_required
def deletemovement(id):
    get_movement(id)
    db = get_db()
    db.execute('DELETE FROM movement WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('inventory.index'))
