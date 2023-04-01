from os import abort

from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from models import *


class ManufacturerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


# TODO:
#   реализовать на каждой из страниц кнопку «Изменить» для изменения производителей/продукции;
#   возможность добавлять/убирать Упаковку(wrapper) прямо со страницы просмотра продукции;
#   реализовать в добавлении продукта выбор цвета и размера упаковки;

# ERROR:
#  нужно спросить про автодискремент(?) при удалении продукции/производителя из БД;
#  решить, как быть с удалением производителей у которого есть продукция. Сейчас не удаляется, выдает ошибку;

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/manufacturers')
def view_manufacturers():
    search_term = request.args.get('search')
    sort_by = request.args.get('sort_by')
    if search_term:
        manufacturers = Manufacturer.query.filter(Manufacturer.manufacturer_name.ilike(f'%{search_term}%')).all()
    else:
        manufacturers = Manufacturer.query.all()

    if not search_term and not sort_by:
        manufacturers = Manufacturer.query.order_by(Manufacturer.manufacturer_id).all()

    if sort_by == 'manufacturer_name':
        manufacturers = sorted(Manufacturer.query.all(), key=lambda m: m.manufacturer_name.lower())

    return render_template('view_manufacturers.html', manufacturers=manufacturers, search_term=search_term,
                           sort_by=sort_by)


@app.route('/manufacturer/add', methods=['GET', 'POST'])
def add_manufacturer():
    form = {"manufacturer_name": "", "submit": False}
    if request.method == 'POST':
        form["manufacturer_name"] = request.form['manufacturer_name']
        form["submit"] = True

        if form["manufacturer_name"]:
            manufacturer = Manufacturer(manufacturer_name=form["manufacturer_name"])
            db.session.add(manufacturer)
            db.session.commit()

            flash('Manufacturer added successfully!', 'success')
            return redirect(url_for('view_manufacturers'))

    return render_template('add_manufacturer.html', form=form)


# ALTER SEQUENCE manufacturer_manufacturer_id_seq RESTART WITH 111;
@app.route('/delete_manufacturer/<int:manufacturer_id>', methods=['POST'])
def delete_manufacturer(manufacturer_id):
    manufacturer = Manufacturer.query.get(manufacturer_id)
    if not manufacturer:
        abort()

    db.session.delete(manufacturer)
    db.session.commit()

    return '', 204


@app.route('/view_products', methods=['GET', 'POST'])
def view_products():
    search_term = request.args.get('search')
    sort_by = request.args.get('sort_by')

    if not search_term and not sort_by:
        products = Product.query.order_by(Product.product_id).all()
    elif sort_by == 'product_name':
        products = Product.query.filter(Product.product_name.like(f"%{search_term}%")).order_by(
            Product.product_name).all()
    elif sort_by == 'manufacturer_name':
        products = Product.query.join(Manufacturer).filter(Product.product_name.like(f"%{search_term}%")).order_by(
            Manufacturer.manufacturer_name).all()
    elif sort_by == 'product_price_asc':
        products = Product.query.filter(Product.product_name.like(f"%{search_term}%")).order_by(
            Product.product_price.asc()).all()
    elif sort_by == 'product_price_desc':
        products = Product.query.filter(Product.product_name.like(f"%{search_term}%")).order_by(
            Product.product_price.desc()).all()
    else:
        products = Product.query.filter(Product.product_name.like(f"%{search_term}%")).all()

    if not products:
        message = 'Ничего не найдено.'
    else:
        message = ''

    return render_template('view_products.html', products=products, search_term=search_term, sort_by=sort_by,
                           message=message)


@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    form = {"product_name": "", "product_price": "", "manufacturer_id": "", "submit": False}
    if request.method == 'POST':
        form["product_name"] = request.form['product_name']
        form["product_price"] = request.form['product_price']
        form["manufacturer_id"] = request.form['manufacturer_id']
        form["submit"] = True

        if form["product_name"] and form["product_price"] and form["manufacturer_id"]:
            product = Product(product_name=form["product_name"], product_price=form["product_price"],
                              manufacturer_id=form["manufacturer_id"])
            db.session.add(product)
            db.session.commit()

            flash('Product added successfully!', 'success')
            return redirect(url_for('view_products'))

    manufacturers = Manufacturer.query.all()
    return render_template('add_product.html', form=form, manufacturers=manufacturers)


# ALTER SEQUENCE product_product_id_seq RESTART WITH 1067;
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        abort(404)

    db.session.delete(product)
    db.session.commit()

    return '', 204


@app.route('/ajax_example', methods=['POST'])
def ajax_example():
    data = request.json
    return jsonify({'response': 'success'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
