from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import json  # json 모듈 임포트

app = Flask(__name__)

# MySQL 연결 설정
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="flask_user",  # 여기에서 'flask_user'를 생성한 사용자 이름으로 변경하세요
            password="your_password",  # 여기에서 'your_password'를 설정한 비밀번호로 변경하세요
            database="flask_app"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# 데이터베이스 테이블 생성 함수
def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            interest VARCHAR(255)
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

create_table()

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Information Form</title>
    </head>
    <body>
        <h1>Submit Your Information</h1>
        <form id="infoForm">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required><br><br>
            
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required><br><br>
            
            <label for="interest">Interest:</label>
            <input type="text" id="interest" name="interest" required><br><br>
            
            <button type="submit">Submit</button>
        </form>

        <script>
            document.getElementById('infoForm').addEventListener('submit', function(event) {
                event.preventDefault();
                
                const formData = {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    interest: document.getElementById('interest').value
                };
                
                fetch('/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            });
        </script>
    </body>
    </html>
    """

# 데이터 저장 함수
def save_data_to_db(data):
    connection = create_connection()
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO submissions (name, email, interest) VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (data['name'], data['email'], data['interest']))
    connection.commit()
    cursor.close()
    connection.close()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    
    # 데이터를 저장합니다.
    save_data_to_db(data)
    
    # 데이터가 저장되는지 콘솔에 출력합니다.
    print(f"Received data: {json.dumps(data, indent=4)}")

    return jsonify({'status': 'success', 'data': data})

@app.route('/data', methods=['GET'])
def get_data():
    data = []
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM submissions")
    rows = cursor.fetchall()
    for row in rows:
        data.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "interest": row[3]
        })
    cursor.close()
    connection.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
