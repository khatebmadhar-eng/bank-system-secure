from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '1234':
            return "تم تسجيل الدخول بنجاح!"
        else:
            return "اسم المستخدم أو كلمة المرور خطأ!"
    
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="اسم المستخدم" required><br>
            <input type="password" name="password" placeholder="كلمة المرور" required><br>
            <input type="submit" value="تسجيل الدخول">
        </form>
    '''
