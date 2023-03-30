from os import abort

from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_wtf import CSRFProtect
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy
from models import *

# csrf = CSRFProtect(app)


# TODO:
#   реализовать добавление/удаление прямо со страницы просмотра продуктов;
#   реализовать на каждой из страниц кнопку «Изменить» для изменения производителей/продуктов
#   .
#   возможность добавлять/убирать теги (wrapper);
#   .
#   доработать закомментированное изменение производителя


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


# ALTER SEQUENCE manufacturer_manufacturer_id_seq RESTART WITH 110;
@app.route('/delete_manufacturer/<int:manufacturer_id>', methods=['POST'])
def delete_manufacturer(manufacturer_id):
    manufacturer = Manufacturer.query.get(manufacturer_id)
    if not manufacturer:
        abort(404)

    db.session.delete(manufacturer)
    db.session.commit()

    return '', 204


# @app.route('/manufacturers/<int:manufacturer_id>/edit', methods=['GET', 'POST'])
# def edit_manufacturer(manufacturer_id):
#     # Получить производителя из базы данных по id
#     manufacturer = Manufacturer.query.get(manufacturer_id)
#
#     # Если метод запроса POST, обновить данные производителя
#     if request.method == 'POST':
#         manufacturer.name = request.form.get('name')
#         db.session.commit()
#         return redirect(url_for('view_manufacturers'))
#
#     # Передать производителя в шаблон edit_manufacturer.html для отображения формы редактирования
#     return render_template('edit_manufacturers.html', manufacturer=manufacturer)
#
#
# @app.route('/manufacturers/<int:manufacturer_id>', methods=['PUT'])
# def update_manufacturer(manufacturer_id):
#     # Получить производителя из базы данных по id
#     manufacturer = Manufacturer.query.get(manufacturer_id)
#     if not manufacturer:
#         abort(404)
#     # Обновить данные производителя
#     manufacturer.name = request.form.get('name')
#     # Сохранить изменения в базе данных
#     db.session.commit()
#     # Вернуть ответ с кодом 200
#     return '', 200


@app.route('/view_products', methods=['GET', 'POST'])
def view_products():
    search_term = request.args.get('search')
    sort_by = request.args.get('sort_by')

    if not search_term and not sort_by:
        products = Product.query.all()
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
        # Если после фильтрации и сортировки ничего не найдено, выводим сообщение об этом
        message = 'Ничего не найдено.'
    else:
        message = ''

    return render_template('view_products.html', products=products, search_term=search_term, sort_by=sort_by,
                           message=message)


@app.route('/ajax_example', methods=['POST'])
def ajax_example():
    data = request.json
    return jsonify({'response': 'success'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
