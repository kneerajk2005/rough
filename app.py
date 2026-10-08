from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "neeraj"




def init_db():
    conn = sqlite3.connect("database.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

db = sqlite3.connect("database.db")

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Execute the query
            cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
            
            # Fetch the result before closing cursor
            result = cursor.fetchone()


            # Check credentials
            if result and result[1] == password:
                session['username'] = result[0]
                return redirect(url_for('home'))
            else:
                error = 'Invalid username or password.'

        except sqlite3.Error as e:
            error = f"SQLite error: {str(e)}"
        
        finally:
            # Safe to close now
            cursor.close()
            conn.close()

    return render_template('login.html', error=error)
    

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/")
def home():
    if 'username' in session:
        return f"Welcome {session['username']}!"
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
