from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

app = Flask(__name__)
app.secret_key = 'MantinOhadToltsis'

# Main page, login box
@app.route('/')
def index():
    return render_template('web_html_sign_in.html')

# route for google sign in
@app.route('/gcallback', methods=['POST'])
def gcallback():
    data = request.get_json()
    token = data.get('credential')
    try:
        # verify token
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), "182999458483-8nv6bv428s0pl8c2a34thvp4qat5ovdh.apps.googleusercontent.com")

        # data base
        user_id = idinfo['sub']
        user_email = idinfo.get('email')

        # check if the user is already exist
        session['user'] = {
            'id': user_id,
            'email': user_email,
            'name': idinfo.get('name')
        }
        return jsonify({ 'success': True })

    except ValueError:
        # not valid token
        return jsonify({ 'success': False }), 400

# example
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    user = session['user']
    return f"Welcome, {user['name']} ({user['email']})!"

if __name__ == '__main__':
    app.run(debug=True)
