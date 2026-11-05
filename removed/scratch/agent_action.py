import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Dashboard</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f0f0;
            text-align: center;
            padding: 50px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            margin: 10px;
            cursor: pointer;
            border: none;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1>Welcome to the Modern Dashboard</h1>
    <button onclick=\"document.body.style.backgroundColor='violet'\">Neon Pink</button>
    <button onclick=\"document.body.style.backgroundColor='cyan'\">Cyber Blue</button>
    <button onclick=\"document.body.style.backgroundColor='lime'\">Toxic Green</button>
</body>
</html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(port=5006)
