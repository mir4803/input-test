from flask import Flask, request, jsonify
import json

app = Flask(__name__)

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
                
                fetch('http://your-ec2-server-ip:5002/submit', {
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

def save_data(data):
    with open('data.json', 'a') as f:
        json.dump(data, f)
        f.write("\n")

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data['name']
    email = data['email']
    interest = data['interest']
    
    # 데이터를 저장합니다.
    save_data(data)

    return jsonify({'status': 'success', 'data': data})

@app.route('/data', methods=['GET'])
def get_data():
    data = []
    with open('data.json', 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
