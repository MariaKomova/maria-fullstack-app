import os
import psycopg2
from flask import Flask, jsonify
from time import sleep
sleep(5) 

app = Flask(__name__)

DB_HOST = os.environ.get('DATABASE_HOST')
DB_USER = os.environ.get('DATABASE_USER')
DB_PASS = os.environ.get('DATABASE_PASSWORD')
DB_NAME = os.environ.get('DATABASE_NAME')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/items', methods=['GET'])
def get_items():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM items;')
        items = cur.fetchall()
        cur.close()
        conn.close()
        
        results = []
        for item in items:
            results.append({'id': item[0], 'name': item[1], 'description': item[2]})
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': 'DB connection failed', 'details': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Backend is up'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

