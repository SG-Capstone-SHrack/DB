import os
import hashlib
from flask import Flask, request, jsonify, render_template, session, redirect
from flask_cors import CORS
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app)
mysql = MySQL(app)

# MySQL 연결 정보 입력
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# 로그인 API
@app.route('/login', methods=['POST'])
def login_api():
    # JSON 데이터 추출
    data = request.get_json()
    id = data['id']
    password = data['password']

    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

    # MySQL 데이터베이스에서 ID 존재하는지 확인
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM members WHERE id = %s AND password = %s"
    val = (id, hashed_password)
    cursor.execute(sql, val)
    existing_member = cursor.fetchone()

    # 데이터베이스에 맞는 ID나 비밀번호가 없는 경우
    if not existing_member:
        return jsonify({'error': '등록되지 않은 사용자입니다.'}), 405

    # 로그인 성공
    return jsonify({'message': '로그인 성공', 'id': existing_member[0]}), 200

# 회원가입 API
@app.route('/signup', methods=['POST'])
def signup_api():
    # JSON 데이터 추출
    data = request.get_json()
    id = data['id']
    password = data['password']
    name = data['name']
    gender = data['gender']
    birthdate = data['birthdate']
    height = data['height']
    weight = data['weight']
    
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

    # MySQL 데이터베이스에서 해당 회원 정보 조회
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM members WHERE id = %s"
    val = (id,)
    cursor.execute(sql, val)
    existing_member = cursor.fetchone()

    if existing_member:
        cursor.close()
        return jsonify({'error': '이미 존재하는 ID입니다.'}), 409

    # MySQL 데이터베이스에 새로운 회원 정보 추가
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO members (id, password, name, gender, birthdate, height, weight) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (id, hashed_password, name, gender, birthdate, height, weight)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

    # HTTP 응답으로 성공 메시지 반환
    return jsonify({'message': 'Signup successful'}), 200

# 운동정보 페이지
@app.route('/exercise_log', methods = ['POST'])
def exercise():
    data = request.get_json()
    print(data)
    id = data["id"]
    date = data["date"]
    
    # 해당 사용자의 운동정보 조회
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM exercise_log WHERE id = %s AND exercise_log.date = %s"
    val = (id, date)

    cursor.execute(sql, val)
    exercise = cursor.fetchall()
    cursor.close()
    
    exercise_list = []
    for row in exercise:
        exercise_dict = {
			'id': row[1],
            'exercise_name': row[5],
            'date': row[2],
            'start_time': row[3],
            'end_time': row[4],
            'exercise_time': row[8],
            'mass': row[6],
            'count': row[7]
        }
        exercise_list.append(exercise_dict)

    return jsonify({'message': 'success', 'exercise_log': exercise_list, 'id': id}), 200

# 운동정보 API
@app.route('/exercise', methods=['POST'])
def exercise_api():
    # JSON 데이터 추출
    data = request.get_json()
    id = data['id']
    date = data['date']
    start_time = data['start_time']
    exercise_time = data['exercise_time']
    end_time = start_time + exercise_time
    exercise_name = data['exercise_name']
    mass = data['mass']
    count = data['count']

    # MySQL 데이터베이스에 새로운 운동 정보 추가
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO exercise_log (id, date, start_time, end_time, exercise_name, mass, count) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (id, date, start_time, end_time, exercise_name, mass, count)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

    # HTTP 응답으로 성공 메시지 반환
    return jsonify({'message': 'Exercise successful'}), 200

if __name__ == '__main__':
    #app.run(host="127.0.0.1", port=5000, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
