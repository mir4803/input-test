from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data['name']
    email = data['email']
    interest = data['interest']
    
    # 여기서 데이터를 처리하거나 데이터베이스에 저장할 수 있습니다.
    print(f"Received data: Name={name}, Email={email}, Interest={interest}")

    return jsonify({'status': 'success', 'data': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
