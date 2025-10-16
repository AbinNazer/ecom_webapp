from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'abin-secret-key'

# Sample products
products = [
    {'id': 1, 'name': 'Wireless Headphones', 'price': 1499, 'image': 'https://i.imgur.com/4YQZ3aK.jpeg'},
    {'id': 2, 'name': 'Smart Watch', 'price': 2499, 'image': 'https://i.imgur.com/bZQq8F7.jpeg'},
    {'id': 3, 'name': 'Bluetooth Speaker', 'price': 999, 'image': 'https://i.imgur.com/ZbQ4A4N.jpeg'},
    {'id': 4, 'name': 'Laptop Stand', 'price': 699, 'image': 'https://i.imgur.com/lz5jM5K.jpeg'}
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart.append(product)
        session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
