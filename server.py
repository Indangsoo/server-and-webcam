from gevent import monkey

monkey.patch_all()

from flask import Flask, request, Response
from flask_cors import CORS
from flask_socketio import SocketIO
from db import Database
import json
from send_push import send_notification

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # CORS 모든 요청 허용

db = Database()


@app.route('/car/danger', methods=["GET"])
def car_danger():
    timestamp = request.args.get("key")  # 쿼리 데이터

    if "." in timestamp:  # 정수 또는 실수로 변환
        timestamp = float(timestamp)
    else:
        timestamp = int(timestamp)

    response = db.insert_car_danger(timestamp)  # DB 삽입

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        socketio.emit("/car/danger", json.dumps({"key": timestamp}))  # 웹소켓으로 정보 보냄
        send_notification("차량 위험 상황", "차량 위험 상황이 발생했습니다.")
        return Response(status=200)  # ok
    else:
        return Response(response.get("data"), status=400)  # Bad


@app.route('/car/danger/data', methods=["GET"])
def car_danger_data():
    response = db.get_car_danger()  # data get

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        return Response(response.get("data"), status=200)  # ok
    else:
        return Response(response.get("data"), status=400)  # Bad


@app.route('/car/open', methods=["GET"])
def car_open():
    timestamp = request.args.get("key")  # 쿼리 데이터

    if "." in timestamp:  # 정수 또는 실수로 변환
        timestamp = float(timestamp)
    else:
        timestamp = int(timestamp)

    response = db.insert_car_open(timestamp)  # DB 삽입

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        socketio.emit("/car/open", json.dumps({"key": timestamp}))  # 웹소켓으로 정보 보냄

        return Response(status=200)  # ok
    else:
        return Response(response.get("data"), status=400)  # Bad


@app.route('/car/open/data', methods=["GET"])
def car_open_data():
    response = db.get_car_open()  # data get

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        return Response(response.get("data"), status=200)  # ok
    else:
        return Response(response.get("data"), status=400)  # Bad


@app.route('/indoor/danger', methods=["GET"])
def indoor_danger():
    timestamp = request.args.get("key")  # 쿼리 데이터

    if "." in timestamp:  # 정수 또는 실수로 변환
        timestamp = float(timestamp)
    else:
        timestamp = int(timestamp)

    response = db.insert_indoor_danger(timestamp)  # DB 삽입

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        socketio.emit("/indoor/danger", json.dumps({"key": timestamp}))  # 웹소켓으로 정보 보냄
        send_notification("실내 위험 상황", "실내 위험 상황이 발생했습니다.\n실시간 영상에서 확인 해 보세요.")
        return Response(status=200)  # ok
    else:
        return Response(response.get("data"), status=400)  # Bad


@app.route('/indoor/danger/data', methods=["GET"])
def indoor_danger_data():
    response = db.get_indoor_danger()  # data get

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        return Response(response.get("data"), status=200)  # ok
    else:
        return Response(response.get("data"), status=400)  # Bad


@app.route('/toilet/towel', methods=["GET"])
def toilet_towel():
    num = int(request.args.get("num"))  # 쿼리 데이터

    response = db.insert_toilet_towel(num)  # DB 삽입

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        socketio.emit("/toilet/towel", json.dumps({"num": num}))  # 웹소켓으로 정보 보냄

        return Response(status=200)  # ok
    else:
        return Response(response.get("data"), status=400)  # Bad


@app.route('/toilet/towel/data', methods=["GET"])
def toilet_towel_data():
    response = db.get_toilet_towel()  # data get

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        return Response(response.get("data"), status=200)  # ok
    else:
        return Response(response.get("data"), status=400)  # Bad


@app.route('/stuff/call', methods=["GET"])
def stuff_call():
    name = request.args.get("name")
    timestamp = request.args.get("key")  # 쿼리 데이터

    if "." in timestamp:  # 정수 또는 실수로 변환
        timestamp = float(timestamp)
    else:
        timestamp = int(timestamp)

    response = db.insert_stuff_call(name, timestamp)  # DB 삽입

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        socketio.emit("/stuff/call", json.dumps({"name": name, "key": timestamp}))  # 웹소켓으로 정보 보냄

        return Response(status=200)  # ok
    else:
        return Response(response.get("data"), status=400)  # Bad


@app.route('/stuff/call/data', methods=["GET"])
def stuff_call_data():
    response = db.get_stuff_call()  # data get

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        return Response(response.get("data"), status=200)  # ok
    else:
        return Response(response.get("data"), status=400)  # Bad


@app.route('/getevents', methods=["GET"])
def getevents():
    response = db.get_events()  # data get

    if response.get("success"):  # DB에 정상적으로 삽입된 경우
        return Response(response.get("data"), status=200)  # ok
    else:
        return Response(response.get("data"), status=400)  # Bad


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

