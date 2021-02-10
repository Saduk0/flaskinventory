from flaskr import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('products', lazy=True))
    productName = db.Column(db.String(80), unique=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # time_created = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return '<Product %r>' % self.productName

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('locations', lazy=True))
    locationName = db.Column(db.String(80), unique=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return '<Location %r>' % self.locationName

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('movements', lazy=True))
    from_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    from_location = db.relationship('Location', backref=db.backref('movementsfrom', lazy=True), foreign_keys=from_location_id)
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    to_location = db.relationship('Location', backref=db.backref('movementsto', lazy=True), foreign_keys=to_location_id)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('movementsproduct', lazy=True), foreign_keys=product_id)
    qty = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return '<Move id %r>' % self.id

def init_models():

    # sample data
    admin = User(username='admin', password='admin')
    db.session.add(admin)
    db.session.commit()
