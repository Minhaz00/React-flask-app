from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://myuser:mypassword@localhost/my_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(200), nullable=True)

# Function to create the database tables
def create_tables():
    with app.app_context():
        db.create_all()

# Call the function to create the tables
create_tables()

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'email': item.email} for item in items])

@app.route('/item', methods=['POST'])
def add_item():
    data = request.json
    new_item = Item(name=data['name'], email=data.get('email', ''))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'id': new_item.id}), 201

@app.route('/item/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.json
    item = Item.query.get(id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404
    item.name = data['name']
    item.email = data.get('email', '')
    db.session.commit()
    return jsonify({'message': 'Item updated'})

@app.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
