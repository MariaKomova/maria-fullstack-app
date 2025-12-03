import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import time
from sqlalchemy.exc import ProgrammingError, OperationalError
from dotenv import load_dotenv
load_dotenv()
from prometheus_client import start_http_server, Summary, Counter, generate_latest

REQUEST_COUNT = Counter(
	'http_request_count',
	'Total HTTP Request Count',
	['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Summary(
	'http_request_latency_seconds',
	'HTTP Request Latency',
	['method', 'endpoint']

)

app = Flask(__name__)


@app.before_request
def start_timer():
	request.start_time = time.time()

@app.after_request
def record_metrics(response):
	if hasattr(request, 'start_time'):
		latency = time.time() - request.start_time
		endpoint = request.path
		method = request.method

		REQUEST_LATENCY.labels(method, endpoint).observe(latency)

		REQUEST_COUNT.labels(method, endpoint, response.status_code).inc()
	
	return response

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value
        }

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        db.session.execute(db.text('SELECT 1')) 
        return jsonify({"status": "ok", "db_status": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "db_status": "disconnected", "detail": str(e)}), 500

@app.route('/metrics', methods=['GET'])
def metrics():
        return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}


@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data or 'value' not in data:
        return jsonify({"error": "Missing name or value"}), 400

    new_item = Item(name=data['name'], value=data['value'])

    try:
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201
    except ProgrammingError as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create item: {e}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/api/items', methods=['GET'])
def get_all_items():
    items = db.session.execute(db.select(Item)).scalars().all()
    return jsonify([item.to_dict() for item in items]), 200

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = db.session.get(Item, item_id)
    
    if item is None:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404

    return jsonify(item.to_dict())

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = db.session.get(Item, item_id)
    
    if item is None:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404

    try:
        db.session.delete(item)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete item: {str(e)}"}), 500

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = db.session.get(Item, item_id)
    
    if item is None:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404

    try:
        if 'name' in data:
            item.name = data['name']
        if 'value' in data:
            item.value = data['value']

        db.session.commit()
        return jsonify(item.to_dict()), 200
    except Exception as e:
        db.session.rollback()

        return jsonify({"error": f"Failed to update item: {str(e)}"}), 500

if __name__ == '__main__':
	time.sleep(5)

	with app.app_context():
		db.create_all()

	start_http_server(8000)
	app.run(host='0.0.0.0', port=5000)

