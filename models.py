from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/BD_confectionery'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'we4fh%gC_za:*8G5v=fbv'
db = SQLAlchemy(app)


class Manufacturer(db.Model):
    __tablename__ = 'manufacturer'
    manufacturer_id = db.Column(db.Integer, primary_key=True, nullable=False)
    manufacturer_name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.manufacturer_name


class Color(db.Model):
    __tablename__ = 'color'
    color_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.name


class Wrapper(db.Model):
    __tablename__ = 'wrapper'
    wrapper_id = db.Column(db.Integer, primary_key=True, nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.color_id'), nullable=False)
    size = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return f"{self.color.name} wrapper"


class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True, nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.manufacturer_id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.Numeric(10, 2), nullable=False)
    manufacturer = db.relationship('Manufacturer', backref='products')

    def __str__(self):
        return self.product_name