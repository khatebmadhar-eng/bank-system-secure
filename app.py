import sqlite3
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def verify_user(username, password):
    db_path = 'bank_secure.db'
    if not os.path.exists(db_path):
        return False
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # نتحقق من وجود المستخدم وكلمة المرور
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None
    except Exception:
        return False

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        
        if verify_user(username, password):
            return "<h1>تم تسجيل الدخول بنجاح! مرحباً بك في نظامك البنكي.</h1>"
        else:
            message = "اسم المستخدم أو كلمة المرور غير صحيحة!"
    
    return render_template_string('''
        <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
            <h2>تسجيل الدخول للنظام البنكي</h2>
            <p style="color: red;">{{ message }}</p>
            <form method="post">
                <input type="text" name="username" placeholder="اسم المستخدم" required><br><br>
                <input type="password" name="password" placeholder="كلمة المرور" required><br><br>
                <input type="submit" value="تسجيل الدخول">
            </form>
        </div>
    ''', message=message)
