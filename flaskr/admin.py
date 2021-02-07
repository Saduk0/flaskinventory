from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('admin',__name__)

@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        'SELECT p.id, productName, amount, created, author_id, username'
        ' FROM product p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    locations = db.execute(
        'SELECT l.id, locationName, created, author_id, username'
        ' FROM location l JOIN user u ON l.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    
    return render_template('admin/index.html', products=products, locations=locations)

@bp.route('/createproduct', methods=('GET', 'POST'))
@login_required
def createproduct():
    if request.method == 'POST':
        productName = request.form['productName']
        amount = request.form['amount']
        error = None

        if not productName:
            error = 'Product name is required.'
        if not amount:
            error = 'Amount is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (productName, amount, author_id)'
                ' VALUES (?, ?, ?)',
                (productName, amount, g.user['id'])
            )
            db.commit()
            return redirect(url_for('admin.index'))
    return render_template('admin/createproduct.html')

def get_product(id, check_author=True):
    product = get_db().execute(
        'SELECT p.id, productName, amount, created, author_id, username'
        ' FROM product p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
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
        amount = request.form['amount']
        error = None
        if not productName:
            error = 'Product Name is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE product SET productName = ?, amount = ?'
                ' WHERE id = ?',
                (productName, amount, id)
            )
            db.commit()
            return redirect(url_for('admin.index'))

    return render_template('admin/updateproduct.html', product=product)

@bp.route('/<int:id>/deleteproduct', methods=('POST',))
@login_required
def deleteproduct(id):
    get_product(id)
    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin.index'))

@bp.route('/<int:id>/', methods=('GET',))
def view(id):
    product = get_product(id, check_author=False)

    return render_template('admin/viewproduct.html', product=product)
