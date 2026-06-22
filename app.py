import sqlite3
from flask import Flask, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def verify_user(username, password):
    conn = sqlite3.connect('bank_secure.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if verify_user(username, password):
            return "<h1>تم تسجيل الدخول بنجاح! مرحباً بك في نظامك البنكي.</h1>"
        else:
            return "<h1>خطأ: اسم المستخدم أو كلمة المرور غير صحيحة.</h1>"
    
    return '''
        <form method="post">
            <h2>تسجيل الدخول للنظام البنكي</h2>
            <input type="text" name="username" placeholder="اسم المستخدم" required><br><br>
            <input type="password" name="password" placeholder="كلمة المرور" required><br><br>
            <input type="submit" value="تسجيل الدخول">
        </form>
    '''
