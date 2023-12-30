from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, template_folder='.')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # 현재 시간 필드 추가
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

@app.route('/')
def index():
    data = SensorData.query.all()
    return render_template('index.html', data=data)

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        temperature = request.form.get('temperature')
        humidity = request.form.get('humidity')
        data = SensorData(temperature=temperature, humidity=humidity, timestamp=datetime.utcnow())  # 현재 시간 저장
        db.session.add(data)
        db.session.commit()
        return 'OK'
    elif request.method == 'GET':
        data = SensorData.query.all()
        return jsonify([{ 'id': d.id, 'temperature': d.temperature, 'humidity': d.humidity, 'timestamp': d.timestamp.isoformat() } for d in data])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)