from flask import Flask, render_template, request, url_for
import json
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sign_up.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    user_data = {'username': username, 'password': password}
    file_path = 'users.json'

    users = []

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                try:
                    users = json.loads(content)
                except json.JSONDecodeError:
                    print("[ERROR] Invalid JSON file. Starting with empty list.")
                    users = []
            else:
                users = []

    users.append(user_data)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

    return render_template('main_page.html', username=username)


@app.route('/signin')
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if os.path.exists('users.json'):
            with open('users.json', 'r', encoding='utf-8') as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []
        else:
            users = []

        for user in users:
            if user['username'] == username:
                if user['password'] == password:
                    return render_template('main_page.html', username=username)
                else:
                    return render_template('sign_in.html', error="Incorrect password.")

        return render_template('sign_in.html', error="Username not found.")

    return render_template('sign_in.html')

@app.route('/main')
def main_page():
    return render_template('main_page.html', username="Guest")

if __name__ == '__main__':
    app.run(debug=True)
