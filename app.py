from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
        <h1>Welcome to the Vulnerable Flask App</h1>
        <form action="/search" method="get">
            Search Users: <input type="text" name="query">
            <input type="submit" value="Search">
        </form>
        <form action="/login" method="post">
            <h2>Login</h2>
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/search')
def search():
    query = request.args.get('query')
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    # Vulnerable to SQL Injection
    c.execute("SELECT username FROM users WHERE username LIKE '%{}%'".format(query))
    results = c.fetchall()
    conn.close()
    return render_template_string("<h1>Search Results</h1><ul>{% for user in results %}<li>{{ user[0] }}</li>{% endfor %}</ul>", results=results)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    # Vulnerable to SQL Injection
    c.execute("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return render_template_string("<h1>Welcome, {}!</h1>".format(user[1]))
    else:
        return '<h1>Login Failed</h1>'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
