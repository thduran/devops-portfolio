import uuid
from flask import Flask, flash, make_response, redirect, render_template, request, url_for
import os
from models.order import Order, OrderItem
from models.product import Product
from models.base import db
from flask_migrate import Migrate, upgrade
import random
from prometheus_client import Info, generate_latest, CONTENT_TYPE_LATEST
import sys
import platform
from metrics import (
    cart_additions_total, 
    errors_total,
    request_duration_histogram,
    update_cpu_usage,
    update_active_sessions
)
import time

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.secret_key = 'supersecretkey'

# Configuração do banco de dados
db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'ecommerce')
db_password = os.getenv('DB_PASSWORD', 'Pg1234')
db_name = os.getenv('DB_NAME', 'ecommerce')
db_port = os.getenv('DB_PORT', 5432)

db_url = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Inicializar SQLAlchemy e Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Configurar métricas Prometheus
app_info = Info('ecommerce_app_info', 'Informações da aplicação e-commerce')
app_info.info({
    'version': '1.0.0',
    'environment': 'development',
    'flask_version': '3.0.0',
    'database_driver': 'postgresql+psycopg'
})

system_info = Info('ecommerce_system_info', 'Informações do sistema')
system_info.info({
    'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    'platform': platform.system(),
    'architecture': platform.machine(),
    'hostname': platform.node()
})

def generate_order_number():
    return f'{random.randint(100000, 999999)}'

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/checkout', methods=['GET'])
def checkout_get():
    order = get_order_from_cookie()

    if not order or not order.items:
        flash("Seu carrinho está vazio. Adicione produtos antes de prosseguir para o checkout.", "warning")
        return redirect(url_for('shop'))

    items = order.items
    subtotal = sum(item.quantity * item.product.price for item in items)
    total = subtotal + 10

    return render_template('checkout.html', items=items, subtotal=subtotal, total=total)


@app.route('/checkout', methods=['POST'])
def checkout():
    user_name = f"{request.form['first_name']} {request.form['last_name']}"
    user_email = request.form['email']
    mobile = request.form['mobile']
    address1 = request.form['address1']
    address2 = request.form.get('address2', '')
    city = request.form['city']
    state = request.form['state']
    country = request.form.get('country', 'Brasil')
    zip_code = request.form['zip']

    card_name = request.form['card_name']
    card_number = request.form['card_number']
    expiry_date = request.form['expiry_date']
    cvv = request.form['cvv']

    order = Order.query.filter_by(is_open=True).first()
    if not order:
        flash("Não há itens no carrinho para finalizar o pedido.", "error")
        return redirect(url_for('cart'))

    order.user_name = user_name
    order.user_email = user_email
    order.mobile = mobile
    order.address1 = address1
    order.address2 = address2
    order.city = city
    order.state = state
    order.country = country
    order.zip_code = zip_code

    order.card_name = card_name
    order.card_number = card_number
    order.expiry_date = expiry_date
    order.cvv = cvv

    order.order_number = generate_order_number()
    order.is_open = False

    db.session.commit()

    # INSTRUMENTAÇÃO GAUGE: Atualizar após checkout
    # DIDÁTICA: Gauge diminui quando sessão é finalizada (diferente de Counter)
    try:
        update_active_sessions()  # Sessão foi fechada, total diminui
    except Exception as e:
        print(f"Erro ao atualizar sessões ativas: {e}")

    flash(f"Pedido realizado com sucesso! Número do pedido: {order.order_number}", "success")
    return redirect(url_for('order_confirmation', order_number=order.order_number))


@app.route('/order_confirmation/<order_number>')
def order_confirmation(order_number):
    order = Order.query.filter_by(order_number=order_number).first()
    return render_template('order_confirmation.html', order=order)

@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

def get_or_create_order():
    uuid_order_id = request.cookies.get('order_id')

    order = None
    response = None

    if uuid_order_id:
        order = Order.query.filter(
            Order.uuid == uuid_order_id, Order.is_open == True
        ).first()

    if not order:
        order = Order(uuid=uuid.uuid4(), total_price=0.0, is_open=True)
        db.session.add(order)
        db.session.commit()

        # INSTRUMENTAÇÃO GAUGE: Atualizar valor atual
        # DIDÁTICA: Gauge precisa ser atualizada quando valor muda
        try:
            update_active_sessions()  # Reconta total de sessões ativas
        except Exception as e:
            print(f"Erro ao atualizar sessões ativas: {e}")

        response = redirect(request.url)
        response.set_cookie('order_id', str(order.uuid))

    return order, response

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        order, response = get_or_create_order()
        quantity = int(request.form.get("quantity"))

        order_item = OrderItem.query.filter_by(order_id=order.id, product_id=product_id).first()

        if order_item:
            order_item.quantity += quantity
        else:
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                price=product.price
            )
            db.session.add(order_item)

        db.session.commit()

        # INSTRUMENTAÇÃO COUNTER: Incrementar quando evento ocorre
        # DIDÁTICA: .inc() só cresce, perfeito para contar adições
        cart_additions_total.labels(product_id=str(product.id)).inc()

        flash(f'{product.name} adicionado ao carrinho!', 'success')

        redirect_response = make_response(redirect(url_for('detail', product_id=product.id)))

        if response:
            for cookie_key, cookie_value in response.headers.items():
                if cookie_key.startswith("Set-Cookie"):
                    redirect_response.headers.add(cookie_key, cookie_value)

        return redirect_response

    except Exception as e:
        # INSTRUMENTAÇÃO COUNTER: Contar erros por tipo
        # DIDÁTICA: Labels classificam erros, facilitam troubleshooting
        errors_total.labels(
            error_type=type(e).__name__,  # Tipo da exceção Python
            endpoint='add_to_cart',       # Onde ocorreu o erro
            status_code='500'             # Status HTTP
        ).inc()
        
        flash('Erro ao adicionar produto ao carrinho', 'error')
        return redirect(url_for('shop'))

@app.route('/detail/<int:product_id>')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.limit(4).all()
    return render_template('detail.html', product=product, related_products=related_products)

def get_order_from_cookie():
    order_id = request.cookies.get('order_id')
    if not order_id:
        return None

    try:
        uuid_order_id = uuid.UUID(order_id)
    except ValueError:
        return None

    return Order.query.filter(
        Order.uuid == str(uuid_order_id), Order.is_open == True
    ).first()


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    order = get_order_from_cookie()
    if not order:
        flash('Seu carrinho está vazio.', 'warning')
        return render_template('cart.html', items=[], subtotal=0, total=0)

    items = order.items
    subtotal = sum(item.quantity * item.price for item in items)
    shipping = 10.0
    total = subtotal + shipping

    return render_template('cart.html', items=items, subtotal=subtotal, total=total)


@app.route('/update_quantity/<int:item_id>', methods=['POST'])
def update_quantity(item_id):
    new_quantity = int(request.form.get('quantity'))
    item = OrderItem.query.get_or_404(item_id)

    if new_quantity <= 0:
        db.session.delete(item)
    else:
        item.quantity = new_quantity

    db.session.commit()
    flash('Quantidade atualizada com sucesso!', 'success')
    return redirect(url_for('cart'))


@app.route('/remove_item/<int:item_id>', methods=['POST'])
def remove_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    flash('Item removido do carrinho.', 'success')
    return redirect(url_for('cart'))


@app.route('/')
def index():
    # INSTRUMENTAÇÃO HISTOGRAM: Medir tempo de resposta
    # DIDÁTICA: Histogram distribui valores em buckets para análise posterior
    start_time = time.time()
    
    try:
        products = Product.query.all()
        response = render_template('index.html', products=products)
        
        duration = time.time() - start_time
        
        # HISTOGRAM: Distribui em buckets, permite agregação no Prometheus
        # DIDÁTICA: Gera _count, _sum e _bucket para cálculo de percentis
        request_duration_histogram.labels(
            method='GET',
            endpoint='index',
            status_code='200'
        ).observe(duration)
        
        return response
        
    except Exception as e:
        # IMPORTANTE: Instrumentar métrica mesmo em caso de erro
        duration = time.time() - start_time
        
        request_duration_histogram.labels(
            method='GET',
            endpoint='index',
            status_code='500'
        ).observe(duration)
        
        raise

@app.route('/metrics')
def metrics():
    # DIDÁTICA: Endpoint especial que expõe métricas para Prometheus
    # PADRÃO: Atualizar Gauges antes de exportar (dados atuais)
    try:
        update_active_sessions()  # Gauge: valor atual de sessões
        update_cpu_usage()        # Gauge: valor atual de CPU
    except Exception as e:
        print(f"Erro ao atualizar métricas: {e}")
    
    # generate_latest(): converte métricas para formato Prometheus
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

def initialize_metrics():
    # DIDÁTICA: Inicializar métricas no startup da aplicação
    # OBJETIVO: Garantir que Gauges tenham valores iniciais corretos
    try:
        update_active_sessions()  # Conta sessões existentes no banco
    except Exception as e:
        print(f"Erro ao inicializar métricas: {e}")

if __name__ == '__main__':
    # PADRÃO: Inicializar métricas antes de aceitar requests
    with app.app_context():  # Context necessário para acessar banco
        initialize_metrics()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
