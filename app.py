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
    if any(u.get('username') == username for u in users):
        return render_template('sign_up.html', error="Username already exists. Please choose another.")

    return render_template('main_page.html', username=username)


@app.route('/signin', methods=['GET','POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 1. טוענים את המשתמשים מהקובץ (או [] אם לא קיים/פגום)
        if os.path.exists('users.json'):
            with open('users.json', 'r', encoding='utf-8') as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []
        else:
            users = []

        # 2. עוברים על כל המשתמשים – בלי else בתוך הלולאה
        for user in users:
            if user.get('username') == username:
                if user.get('password') == password:
                    return render_template('main_page.html', username=username)
                else:
                    return render_template('sign_in.html', error="Incorrect password.")
        # 3. אם לא מצאנו בכלל שם תואם, חוזרים עם שגיאת “not found”
        return render_template('sign_in.html', error="Username not found.")
    else:
        # GET רגיל – מציגים את טופס ה־signin
        return render_template('sign_in.html')


@app.route('/main')
def main_page():
    return render_template('main_page.html', username="Guest")

if __name__ == '__main__':
    app.run(debug=True)
