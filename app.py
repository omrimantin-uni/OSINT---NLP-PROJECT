from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sign_in.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    print(f"[INFO] Logged in as: {username}")
    return render_template('main_page.html', username=username)



@app.route('/debug-css')
def debug_css():
    return f"Resolved CSS URL: {url_for('static', filename='sign_in.css')}"

if __name__ == '__main__':
    app.run(debug=True)
