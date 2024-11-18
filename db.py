import sqlite3

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
                CREATE TABLE IF NOT EXISTS car (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    danger INTEGER
                )
                ''') # car 테이블 생성
                # TODO
                #  추가 테이블
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

    def get_data(self, table_name, column, order_by):
        '''필요 데이터 get'''
        try:  # 예외처리
            with sqlite3.connect(self.db_file) as conn:  # with문으로 conn 사용후 닫음
                cursor = conn.cursor()

                query = f"SELECT {column} FROM {table_name} ORDER BY {order_by} DESC LIMIT 1"  # 가장 최근 데이터 쿼리

                cursor.execute(query)  # 실행

                data = tuple(cursor.fetchone())  # 최근 데이터 한개

                return ResponseModel(True, str(data[0])).dict()  # 딕셔너리 형태로 응답
        except sqlite3.OperationalError as e:  # 오류 발생한 경우
            return ResponseModel(False, str(e)).dict()

    def insert_car_danger(self, timestamp):
        '''/car/danger DB 삽입'''
        return self.insert_data("car", ["danger"], [timestamp])

    def get_car_danger(self):
        '''/car/danger 값 get'''
        return self.get_data("car", "danger", "danger")

    # TODO  # 인서트 함수 추가
