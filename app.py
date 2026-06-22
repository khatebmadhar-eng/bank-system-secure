import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('bank_secure.db')
    cursor = conn.cursor()
    # إنشاء الجدول إذا لم يكن موجوداً
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    # إضافة مستخدم تجريبي إذا لم يكن موجوداً
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users VALUES ('admin', '1234')")
        conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect('bank_secure.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
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
