from flask import Flask, request, render_template, jsonify
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use Render's DATABASE_URL, fallback to local for development
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:torontomet123@localhost/anime_hub_db'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define order model mapped to existing table
class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    package = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

# Test route
@app.route('/test', methods=['GET'])
def test_route():
    return 'Flask app is working and connected to PostgreSQL'

@app.route('/')
def index():
    return render_template('index.html')

# Order submission route
@app.route('/submit', methods=['POST'])
def submit_order():
    name = request.form['name']
    address = request.form['address']
    package = request.form['package']
    region = request.form['region']
    
    package_prices = {
        "Anniversary Comic Book": 400,
        "Comic Book Package": 800,
        "Anniversary Anime Package": 1500,
        "Deluxe Package": 3000,
        "Mystery Package": 1000
    }

    shipping_prices = {
        "North America": 150,
        "Europe": 200,
        "Asia": 100
    }

    if package not in package_prices or region not in shipping_prices:
        return jsonify({"error": "Invalid package or region"}), 400

    total_price = package_prices[package] + shipping_prices[region]

    new_order = Order(
        name=name,
        address=address,
        package=package,
        region=region,
        total_price=total_price
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        "message": "Order placed successfully!",
        "total_price": f"{total_price} GYD",
        "price_breakdown": {
            "package_price": f"{package_prices[package]} GYD",
            "shipping_price": f"{shipping_prices[region]} GYD"
        }
    })

# Route to list all orders
@app.route('/orders', methods=['GET'])
def all_orders():
    result_set = db.session.query(Order).all()
    return jsonify([
        {
            "id": row.id,
            "name": row.name,
            "address": row.address,
            "package": row.package,
            "total_price": row.total_price
        }
        for row in result_set
    ])

# ✅ Automatically create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

