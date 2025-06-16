from flask import Flask, request, render_template, jsonify

from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:torontomet123@localhost/anime_hub_db'
db = SQLAlchemy(app)

# define order model mapped to existing table
class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    package = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

# test route to termine if flask is initialized properly 
# http://localhost:5000/test
@app.route('/test', methods=['GET'])
def test_route() :
    return 'Flask app is working and connected to PostgreSQL'

@app.route('/')
def index():
    return render_template('index.html')

    
# route to handle order submissions
@app.route('/submit', methods=['POST'])
def submit_order():
    selected_package = request.form['package'] # gets dropdown value

    
    name = request.form['name']
    address = request.form['address']
    package = request.form['package']
    region = request.form['region']
    
    # package and shipping prices 
    package_prices = {
        "Anniversary Comic Book": 400,
        "Comic Book Package": 800,
        "Anniversary Anime Package": 1500,
        "Deluxe Package": 3000,
        "Mystery Package": 1000
    }
    
    # defining shipping prices
    shipping_prices = {
        "North America": 150,
        "Europe": 200,
        "Asia": 100
    }
    
    # calculating total price
    if package not in package_prices or region not in shipping_prices:
        return jsonify({"error": "Invalid package or region"}), 400
        
    total_price = package_prices[package] + shipping_prices[region]
    
    # inserting into database
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

# a route to list all orders
# http://localhost:500/orders
@app.route('/orders', methods=['GET'])
def all_orders():
    result_set = db.session.query(Order).all()
    
    order_list = []
    for row in result_set:
        order_list.append({
            "id": row.id,
            "name": row.name,
            "address": row.address,
            "package": row.package,
            "total_price": row.total_price
        })
    return jsonify(order_list)
    
if __name__ == '__main__':
    app.run(debug=True)
