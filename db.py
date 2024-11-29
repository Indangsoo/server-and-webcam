import sqlite3
import time
import json

from db_response_model import ResponseModel

DB_FILE = 'data.db'  # DB 파일


class Database:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        '''DB 초기화'''
        try:  # 예외처리
            with sqlite3.connect(self.db_file) as conn:  # with문으로 conn 사용후 닫음
                cursor = conn.cursor()
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS event (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    place TEXT NOT NULL,
                    key NUMERIC NOT NULL
                )
                ''') # event 테이블 생성
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS towel (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    num INTEGER NOT NULL,
                    time NUMERIC NOT NULL
                )
                ''') # towel 테이블 생성
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS stuff_call (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    key NUMERIC NOT NULL
                )
                ''') # stuff_call 테이블 생성
                conn.commit()  # 저장
                return ResponseModel(True, None).dict()  # 딕셔너리 형태로 응답
        except sqlite3.OperationalError as e:  # 오류 발생한 경우
            return ResponseModel(False, str(e)).dict()

    def insert_data(self, table_name, columns, values):
        '''주어진 데이터 삽입'''
        try:  # 예외처리
            with sqlite3.connect(self.db_file) as conn:  # with문으로 conn 사용후 닫음
                cursor = conn.cursor()

                columns_str = ", ".join(columns)  # 컬럼 이름
                placeholders = ", ".join(["?"] * len(values))  # 자리표시자

                query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"  # 컬럼에 값 삽입 쿼리

                cursor.execute(query, values)  # 실행

                conn.commit()  # 저장
                return ResponseModel(True, None).dict()  # 딕셔너리 형태로 응답
        except sqlite3.OperationalError as e:  # 오류 발생한 경우
            return ResponseModel(False, str(e)).dict()

    def get_data(self, table_name, find_columns, order_by, search_q=None):
        '''필요 데이터 get'''
        try:  # 예외처리
            with sqlite3.connect(self.db_file) as conn:  # with문으로 conn 사용후 닫음
                conn.row_factory = sqlite3.Row

                cursor = conn.cursor()

                columns_str = ", ".join(find_columns)  # 컬럼 이름

                if search_q:
                    query = f"SELECT {columns_str} FROM {table_name} WHERE {search_q} ORDER BY {order_by} DESC LIMIT 1"  # 가장 최근 데이터 쿼리
                else:
                    query = f"SELECT {columns_str} FROM {table_name} ORDER BY {order_by} DESC LIMIT 1"  # 가장 최근 데이터 쿼리

                cursor.execute(query)  # 실행

                row = cursor.fetchone()  # 최근 데이터 한개

                if row:
                    data = dict(row)

                return ResponseModel(True, str(data)).dict()  # 딕셔너리 형태로 응답
        except sqlite3.OperationalError as e:  # 오류 발생한 경우
            return ResponseModel(False, str(e)).dict()

    def insert_car_danger(self, timestamp):
        return self.insert_data("event", ["type", "place", "key"], ["danger", "car", timestamp])

    def get_car_danger(self):
        return self.get_data("event", ["key"], "key", "type = 'danger' AND place = 'car'")

    def insert_car_open(self, timestamp):
        return self.insert_data("event", ["type", "place", "key"], ["open", "car", timestamp])

    def get_car_open(self):
        return self.get_data("event", ["key"], "key", "type = 'open' AND place = 'car'")

    def insert_indoor_danger(self, timestamp):
        return self.insert_data("event", ["type", "place", "key"], ["danger", "indoor", timestamp])

    def get_indoor_danger(self):
        return self.get_data("event", ["key"], "key", "type = 'danger' AND place = 'indoor'")

    def insert_toilet_towel(self, num):
        return self.insert_data("towel", ["num", "time"], [num, time.time()])

    def get_toilet_towel(self):
        return self.get_data("towel", ["num"], "time")

    def insert_stuff_call(self, stuff_name, timestamp):
        return self.insert_data("stuff_call", ["name", "key"], [stuff_name, timestamp])

    def get_stuff_call(self):
        return self.get_data("stuff_call", ["name", "key"], "key")

    def get_events(self):
        try:  # 예외처리
            with sqlite3.connect(self.db_file) as conn:  # with문으로 conn 사용후 닫음
                conn.row_factory = sqlite3.Row

                cursor = conn.cursor()

                # 모든 데이터 union 후 내림차순 정렬
                query = '''
                SELECT
                    event.key AS time,
                    CASE 
                        WHEN event.type = 'danger' AND event.place = 'car' THEN 'car_danger'
                        WHEN event.type = 'open' AND event.place = 'car' THEN 'car_open'
                        WHEN event.type = 'danger' AND event.place = 'indoor' THEN 'indoor_danger'
                    END AS event_type,
                    NULL AS data
                FROM event
                UNION ALL
                SELECT
                    towel.time AS time,
                    'towel_change' AS event_type,
                    towel.num AS data
                FROM towel    
                UNION ALL 
                SELECT
                    stuff_call.key AS time,
                    'stuff_call' AS event_type,
                    stuff_call.name AS data
                FROM stuff_call
                ORDER BY time DESC
                '''

                cursor.execute(query)  # 실행

                row = cursor.fetchall()  # 최근 데이터 전체

                if row:
                    data = list(map(lambda x: dict(x), row))  # 리스트 내 데이터 딕셔너리 형태로 변경

                return ResponseModel(True, json.dumps(data)).dict()  # json 형태로 응답
        except sqlite3.OperationalError as e:  # 오류 발생한 경우
            return ResponseModel(False, str(e)).dict()