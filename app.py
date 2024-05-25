from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# 데이터 파일 경로 설정 (루트 디렉토리)
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data.json')

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
def save_data(data):
    if not os.path.exists(DATA_FILE_PATH) or os.stat(DATA_FILE_PATH).st_size == 0:
        with open(DATA_FILE_PATH, 'w') as f:
            json.dump([data], f, indent=4)
    else:
        with open(DATA_FILE_PATH, 'r+') as f:
            file_data = json.load(f)
            file_data.append(data)
            f.seek(0)
            json.dump(file_data, f, indent=4)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    
    # 데이터를 저장합니다.
    save_data(data)
    
    # 데이터가 저장되는지 콘솔에 출력합니다.
    print(f"Received data: {json.dumps(data, indent=4)}")

    return jsonify({'status': 'success', 'data': data})

@app.route('/data', methods=['GET'])
def get_data():
    data = []
    if os.path.exists(DATA_FILE_PATH) and os.stat(DATA_FILE_PATH).st_size != 0:
        with open(DATA_FILE_PATH, 'r') as f:
            data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
