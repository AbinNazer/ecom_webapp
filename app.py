from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, os, uuid

app = Flask(__name__)

DATA_FILE = 'products.json'


# 🧠 Load Products
def load_products():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


# 💾 Save Products
def save_products(products):
    with open(DATA_FILE, 'w') as f:
        json.dump(products, f, indent=4)


@app.route('/')
def home():
    return redirect(url_for('products'))


# 🛍 Show all products with optional filters
@app.route('/products')
def products():
    products = load_products()
    search = request.args.get('search', '').lower()
    category = request.args.get('category', '')

    if search:
        products = [p for p in products if search in p['name'].lower()]

    if category:
        products = [p for p in products if p['category'] == category]

    categories = sorted(set([p['category'] for p in products]))
    return render_template('products.html', products=products, categories=categories)


# ➕ Add Product (form + save)
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        products = load_products()
        new_product = {
            "id": str(uuid.uuid4()),
            "name": request.form['name'],
            "price": float(request.form['price']),
            "original_price": request.form.get('original_price', ''),
            "description": request.form['description'],
            "category": request.form['category'],
            "discount": request.form.get('discount', ''),
            "rating": int(request.form.get('rating', 5)),
            "image": request.form['image']
        }
        products.append(new_product)
        save_products(products)
        return redirect(url_for('products'))

    return render_template('add_product.html')


# 🛒 Add to cart (mock route)
@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    return f"✅ Product {product_id} added to cart! (Mock action)"


# 🔄 API Endpoint (optional for future use)
@app.route('/api/products')
def api_products():
    return jsonify(load_products())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
