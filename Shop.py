from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pcharmacy.db'    # Установка URL адреса для БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # Отключение отслеживания изменений в БД
app.secret_key = "My Secret key"    # Задаём секретный ключ для подписей session
app.config['SESSION_TYPE'] = 'filesystem'   # Установка типа хранения сессий(файловая система)
Session(app)
db = SQLAlchemy(app)    # Создание экземпляра для работы с БД
app.app_context().push()
migrate = Migrate(app, db, command='migrate')   # Создаём экземпляр для обработки миграций БД
sess = Session()    # Создание экземпляр Session для работы с сессиями


class Medecine(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(255), nullable=False)
     price = db.Column(db.Float, nullable=False)
     text = db.Column(db.Text, nullable=False)
     item_image_path = db.Column(db.String(255), nullable=False)


product1 = Medecine(title='Циклоферон', price=266.99, text=' Способствует сокращению частоты, выраженности и длительности вирусных инфекций, в том числе простуды и гриппа.', item_image_path='images/cikloferon.png')
product2 = Medecine(title='Доктор МОМ', price=191.99, text='Обладает комплексным действием: выводит мокроту, очищает бронхи и снимает воспаление.', item_image_path='images/Doctor_mom.png')
product3 = Medecine(title='Полисорб', price=565.99, text='Препарат эффективен при лечении диареи, отравлений, аллергии, токсикоза, похмельного синдрома и при комплексном очищении организма.', item_image_path='images/полисорб.jpg')
product4 = Medecine(title='Гексорал', price=268.99, text='Препарат обладает противовирусным действием в отношении вирусов гриппа А, респираторно-синцитиального вируса (РС-вирус), вируса простого герпеса 1-го типа, поражающих респираторный тракт.', item_image_path='images/gecsoral.png')
product5 = Medecine(title='Фарингосепт', price=237.99, text='Симптоматическое лечение инфекционно-воспалительных заболеваний полости рта и глотки: тонзиллит, гингивит, стоматит, фарингит.', item_image_path='images/faringosept.png')


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

        error_message = None

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


if __name__ == "__main__":  # Проверка: является ли этот file.py - главным(если да, то код выполняется)
     with app.app_context():
          db.create_all()   # Создание всех таблиц в БД
          sess.init_app(app)    # Инициализируем сессию
          if not Medecine.query.first():    # Проверка на заполненность товаров БД
              db.session.add(product1)
              db.session.add(product2)
              db.session.add(product3)
              db.session.add(product4)
              db.session.add(product5)
              db.session.commit()
     app.run(debug=True)    # Запуск сервера с выключенным режимом отладки
