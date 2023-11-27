from flask import render_template, url_for, request, redirect, session, jsonify
from main import app
from models import Medecine


@app.route('/')
def index():
    # Получение данных о товарах из базы данных
    products = Medecine.query.limit(5).all()
    print(url_for('index'))
    return render_template('front.html', products=products)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        cart_number = request.form.get('card_number')
        cardholder_name = request.form.get('cardholder_name')
        expiration_date = request.form.get('expiration_date')
        cvs = request.form.get('cvs')

        session.pop('cart', None)

        #error_message = None

        if not(cart_number and cardholder_name and expiration_date and cvs):
            error_message = 'Пожалуйста, заполните поля правильно!'

            return render_template('payment.html', error_message=error_message)
        session['cart_count'] = 0
        return render_template('itog.html', success_message=f'Оплата прошла успешно!')

    else:
        return render_template('payment.html')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'cart' in session and session['cart']:
        products = []
        total_cost = 0
        for product_id in session['cart']:
            product = Medecine.query.get(product_id)
            products.append(product)
            total_cost += product.price * session['cart'][product_id]
        return render_template('cart.html', products=products, total_cost=total_cost)
    return render_template('cart.html', products=None, total_cost=0)


@app.route('/cart/<int:product_id>', methods=['POST'])
def cart_add(product_id):    # 1
    if 'cart' not in session:
        session['cart'] = {}    # {1: 1}

    if product_id in session['cart']:
        session['cart'][product_id] += 1    # {1: 2}
    else:
        session['cart'][product_id] = 1

    session['cart_count'] = sum(session['cart'].values())    # Обновление сессии кол-ва товаров в корзине
    return redirect('/')


@app.route('/cart/delete/<int:product_id>', methods=['POST'])
def cart_delete(product_id):
    if product_id in session['cart'] and session['cart'][product_id] > 1:
        session['cart'][product_id] -= 1
    else:
        del session['cart'][product_id]
    session['cart_count'] = sum(session['cart'].values())
    return redirect('/cart')


@app.route('/cart/count')
def cart_count():
    cart_count = session.get('cart_count', 0)
    return jsonify(cart_count=cart_count)


if __name__ == '__main__':
    app.run()
    