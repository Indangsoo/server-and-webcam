from gevent import monkey
monkey.patch_all()

from flask import Flask, request, Response
from flask_cors import CORS
from flask_socketio import SocketIO
from db import Database

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # CORS 모든 요청 허용

db = Database()

@app.route('/car/danger', methods=["GET"])
def car_danger():
    timestamp = request.args.get("key")  # 쿼리 데이터

    response = db.insert_car_danger(timestamp)  # DB 삽입

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        socketio.emit("/car/danger", timestamp)  # 웹소켓으로 정보 보냄

        return Response(status=200)  # ok
    else:
        return Response(response.get("data"),status=400)  # Bad

@app.route('/car/danger/data', methods=["GET"])
def car_danger_data():
    response = db.get_car_danger()  # data get

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        return Response(response.get("data") ,status=200)  # ok
    else:
        return Response(status=400)  # Bad



#TODO
# route 추가

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

