from flask import Flask, render_template, request, make_response, abort, redirect
import json
import re

app = Flask(__name__)


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return True if re.match(email_regex, email) else False


@app.post('/login/')
def login_func():
    login = request.form.get('login')
    email = request.form.get('email')
    if not login or not email or not is_valid_email(email):
        abort(400, 'Неверные данные!')
    with open('users.json', 'r+') as f:
        users = json.load(f)
        users[login] = email
        f.seek(0)
        json.dump(users, f, indent=4)
    response = make_response(redirect('/hello'))
    response.set_cookie('user', login)
    return response


@app.route('/')
@app.route('/hello')
def hello():
    login = request.cookies.get('user')
    if login:
        return render_template('hello.html', username=login)
    else:
        return render_template('login.html')


@app.route('/logout/')
def logout():
    response = make_response(redirect('/'))
    response.set_cookie('user', '',  expires=0)
    return response


if __name__ == '__main__':
    app.run(debug=True)
