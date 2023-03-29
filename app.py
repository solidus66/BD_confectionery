from flask import render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy
from models import *


# TODO:
#   реализовать добавление/удаление прямо со страниц просмотра производителей/продуктов;
#   реализовать на каждой из страниц кнопку «Изменить» для выбора производителей/продуктов, которые
#   нужно удалить;
#   возможность редактировать по клику;
#   возможность добавлять/убирать теги (wrapper);


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
