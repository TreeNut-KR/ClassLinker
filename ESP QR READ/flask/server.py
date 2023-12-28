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
    timestamp = db.Column(db.DateTime, default=datetime.now)  # 현재 서버 컴퓨터의 로컬 시간 필드 추가
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

@app.route('/')
def index():
    data = SensorData.query.all()
    return render_template('index.html', data=data)

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        temperature = request.args.get('temperature')  # change this line
        humidity = request.args.get('humidity')  # and this line
        data = SensorData(temperature=temperature, humidity=humidity, timestamp=datetime.now())
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