from flask import Flask, request, jsonify

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
                
                fetch('http://15.165.180.185:5002/submit', {
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
