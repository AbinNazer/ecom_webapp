from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# =====================
# 🖼️ Configuration for image uploads
# =====================
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =====================
# 🛒 In-memory database
# =====================
products = [
    {
        'id': 1,
        'name': 'Sample Product 1',
        'price': 499,
        'original_price': 599,
        'discount': 20,
        'rating': 4,
        'category': 'Electronics',
        'image': '/static/images/sample1.jpg'
    },
    {
        'id': 2,
        'name': 'Sample Product 2',
        'price': 299,
        'original_price': None,
        'discount': None,
        'rating': 5,
        'category': 'Books',
        'image': '/static/images/sample2.jpg'
    }
]

categories = ['Electronics', 'Books', 'Clothing', 'Toys']
cart = []

# =====================
# 🧩 Helper Functions
# =====================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =====================
# 🌐 Routes
# =====================

@app.route('/')
def index():
    return render_template('index.html', products=products[:4], cart=cart)

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

@app.route('/cart')
def cart_page():
    return render_template('cart.html', cart=cart)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart.append(product)
    return redirect(url_for('cart_page'))

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
            image_url = '/static/images/default.png'

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


# =====================
# 🧠 Local AI Chatbot (No API)
# =====================
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "").lower()

    if not user_message:
        return jsonify({"reply": "Please type something!"})

    # Simple keyword-based responses
    if "price" in user_message:
        reply = "You can check the price on each product card. Would you like me to show discounts too?"
    elif "discount" in user_message:
        reply = "We have great discounts up to 25%! Check out the 'Smartphone' section."
    elif "order" in user_message or "buy" in user_message:
        reply = "You can add items to your cart and proceed to checkout!"
    elif "hello" in user_message or "hi" in user_message:
        reply = "Hello there! 👋 How can I help you today?"
    elif "help" in user_message:
        reply = "Sure! You can browse products, add them to your cart, or ask me about deals."
    else:
        reply = "I'm your shopping assistant 🤖 — ask me about products, prices, or discounts!"

    return jsonify({"reply": reply})


# =====================
# 🚀 Main Runner
# =====================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

