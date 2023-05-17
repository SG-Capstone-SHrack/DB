import os
import hashlib
from flask import Flask, request, jsonify, render_template, session, redirect
from flask_cors import CORS
from flask_mysqldb import MySQL
from dotenv import load_dotenv

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

# 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 로그인 페이지
@app.route('/login')
def login():
    return render_template('login.html')

# 로그인 API
@app.route('/login', methods=['POST'])
def login_api():
    # HTTP 요청으로부터 필요한 데이터 추출
    id = request.form['id']
    password = request.form['password']

    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

    # MySQL 데이터베이스에서 해당 회원 정보 추출
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM members WHERE id = %s AND password = %s"
    val = (id, hashed_password)
    cursor.execute(sql, val)
    member = cursor.fetchone()
    cursor.close()

    # 해당 회원 정보가 없는 경우
    if member is None:
        return jsonify({'message': 'Login failed'}), 400

    # 해당 회원 정보가 있는 경우
    else:
        session['user_id'] = id
        return redirect('/exercise')

# 회원가입 페이지
@app.route('/signup')
def siguup():
    return render_template('signup.html')

# 회원가입 API
@app.route('/signup', methods=['POST'])
def signup_api():
    # HTTP 요청으로부터 필요한 데이터 추출
    id = request.form['id']
    password = request.form['password']
    name = request.form['name']
    gender = request.form['gender']
    birthdate = request.form['birthdate']
    height = request.form['height']
    weight = request.form['weight']
    email = request.form['email']
    
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

    # MySQL 데이터베이스에 새로운 회원 정보 추가
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO members (id, password, name, gender, birthdate, height, weight, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (id, hashed_password, name, gender, birthdate, height, weight, email)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

    # HTTP 응답으로 성공 메시지 반환
    return jsonify({'message': 'Signup successful'}), 200

# 운동정보 페이지
@app.route('/exercise')
def exercise():
    user_id = session.get('user_id')
    
    # 로그인하지 않은 경우 로그인 페이지로 리다이렉트
    if user_id is None:
        return redirect('/login')
    
    # 해당 사용자의 운동정보 조회
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM exercise_log JOIN exercise ON exercise_log.exercise_code = exercise.exercise_code WHERE id = %s"
    val = (user_id,)
    cursor.execute(sql, val)
    exercise = cursor.fetchall()
    cursor.close()
    
    return render_template('exercise.html', exercise = exercise)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)