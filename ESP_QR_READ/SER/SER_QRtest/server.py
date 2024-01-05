from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_caching import Cache

app = Flask(__name__, static_folder="./", template_folder="./")
socketio = SocketIO(app)

# 캐시 설정
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

def custom_cache_key():
    return request.get_json().get('qrcode', '')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/QR', methods=['POST'])
@cache.cached(timeout=50, key_prefix=custom_cache_key)  # 이 API 응답을 50초 동안 캐시합니다.
def api():
    data = request.get_json()  # JSON 형태로 전송된 데이터를 받아옵니다.
    qr_code_value = data.get('qrcode', '')  # 'qrcode' 키의 값을 가져옵니다.
    
    # QR 코드 값을 소켓을 통해 클라이언트에게 전송합니다.
    socketio.emit('update', {'qr_code': qr_code_value})
    
    return jsonify(data), 200  # 받아온 데이터를 그대로 반환합니다.

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5100)
