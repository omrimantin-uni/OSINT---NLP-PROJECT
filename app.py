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



    if any(u.get('username') == username for u in users):
        return render_template('sign_up.html', error="Username already exists. Please choose another.")
    users.append({'username': username, 'password': password})
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

    return render_template('main_page.html', username=username)


@app.route('/signin', methods=['GET','POST'])
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
            if user.get('username') == username:
                if user.get('password') == password:
                    return render_template('main_page.html', username=username)
                else:
                    return render_template('sign_in.html', error="Incorrect password.")

        return render_template('sign_in.html', error="Username not found.")
    else:

        return render_template('sign_in.html')


@app.route('/main')
def main_page():
    return render_template('main_page.html', username="Guest")

@app.route('/logout')
def logout():
    return render_template('sign_in.html')
if __name__ == '__main__':
    app.run(debug=True)