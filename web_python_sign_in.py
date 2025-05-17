from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

app = Flask(__name__)
app.secret_key = 'SECRET_KEY_YOUR_CHOICE'

# העמוד הראשי עם ה-login-box
@app.route('/')
def index():
    return render_template('web_html_sign_in.html')

# Route לטיפול ב-Google Sign In
@app.route('/gcallback', methods=['POST'])
def gcallback():
    data = request.get_json()
    token = data.get('credential')
    try:
        # אימות הטוקן מול Google
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), "YOUR_CLIENT_ID_HERE")

        # idinfo יכיל שדות כמו 'sub' (id ייחודי למשתמש), 'email', 'name' וכו'
        user_id = idinfo['sub']
        user_email = idinfo.get('email')

        # כאן תוכל/י לבדוק במסד נתונים אם המשתמש קיים, ליצור משתמש חדש, וכו'
        session['user'] = {
            'id': user_id,
            'email': user_email,
            'name': idinfo.get('name')
        }
        return jsonify({ 'success': True })

    except ValueError:
        # טוקן לא תקין
        return jsonify({ 'success': False }), 400

# דוגמה לדף המוגן
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    user = session['user']
    return f"Welcome, {user['name']} ({user['email']})!"

if __name__ == '__main__':
    app.run(debug=True)
