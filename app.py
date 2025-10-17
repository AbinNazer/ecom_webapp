from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for image uploads
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# In-memory products list
products = [
    {
        'id': 1,
        'name': 'Smartphone',
        'price': 14999,
        'original_price': 19999,
        'discount': 25,
        'rating': 4,
        'category': 'Electronics',
        'image': '/static/images/sample1.jpg'
    },
    {
        'id': 2,
        'name': 'Book: Python Basics',
        'price': 499,
        'original_price': None,
        'discount': None,
        'rating': 5,
        'category': 'Books',
        'image': '/static/images/sample2.jpg'
    }
]

categories = ['Electronics', 'Books', 'Clothing', 'Toys']
cart = []

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page
@app.route('/')
def index():
    return render_template('index.html', products=products, categories=categories, cart=cart)

# Products page
@app.route('/products')
def products_page():
    search = request.args.get('search', '').lower()
    category = request.args.get('category', '')

    filtered_products = products
    if search:
        filtered_products = [p for p in filtered_products if search in p['name'].lower()]
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]

    return render_template('products.html', products=filtered_products, categories=categories, cart=cart)

# Cart page
@app.route('/cart')
def cart_page():
    return render_template('cart.html', cart=cart)

# Add to cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart.append(product)
    return redirect(url_for('cart_page'))

# Add new product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        original_price = request.form.get('original_price')
        original_price = float(original_price) if original_price else None
        discount = request.form.get('discount')
        discount = int(discount) if discount else None
        rating = int(request.form.get('rating', 0))
        category = request.form.get('category', 'Misc')
        image_file = request.files['image']

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_url = f'/static/images/{filename}'
        else:
            image_url = '/static/images/default.png'  # default image

        new_product = {
            'id': max(p['id'] for p in products) + 1 if products else 1,
            'name': name,
            'price': price,
            'original_price': original_price,
            'discount': discount,
            'rating': rating,
            'category': category,
            'image': image_url
        }
        products.append(new_product)
        return redirect(url_for('products_page'))

    return render_template('add_product.html', categories=categories, cart=cart)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
