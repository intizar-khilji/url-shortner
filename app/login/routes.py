from flask import render_template, request, redirect, url_for
from . import login, home_url
from .database import authenticate_user, change_password, create_new_user, generate_otp, get_otp_count, is_user_exist
from .functions import send_mail
from app import session

@login.route('/login', methods=['POST', 'GET'])
def login_page():
    if 'user' in session:
        return redirect(url_for(home_url))
    res = eval(request.args.get('res')) if request.args.get('res') else None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        id = authenticate_user(email, password)
        if id:
            session['user'] = id
            return redirect(url_for('login.login_page'))
        else:
            res = {'response' : 'error', 'message' : 'Username or Password is wrong'}
    return render_template('login.html', res=res)

@login.route('/signup', methods=['POST', 'GET'])
def signup():
    if 'user' in session:
        return redirect(url_for(home_url))
    res = None
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        if name and email and password and len(password) > 7:
            if is_user_exist(email):
                res = {'response' : 'error', 'message' : 'This email has been already used', 'email' : email}
            else:
                create_new_user(name, email, password)
                return redirect(url_for('login.login_page', res={"response" : "success", "message" : "Successfully registered"}))
        else:
            return redirect(url_for('login.login_page', res={"response" : "error", "message" : "Something wrong"}))
    return render_template('signup.html', res=res)

@login.route('/forgot-password', methods=['POST', 'GET'])
def forgot_password():
    res = None
    if 'user' in session:
        return redirect(url_for(home_url))
    if request.method == 'POST':
        email = request.form.get('email')
        id = is_user_exist(email)
        if id:
            count, _ = get_otp_count(id)
            if count > 2:
                res = {'response' : 'error', 'message' : 'Too many otps generated.\nPlease wait for 10 minutes.'}
            else:
                otp = generate_otp(id)
                send_mail([email], {'subject' : 'Forgot Password OTP', 'message' : f'Your OTP is {otp}'})
                res = {'response' : 'success', 'message' : 'OTP Sent','email' : email, 'origin':'forgot-password'}
                return render_template('otp-verification.html', res=res)
        else:
            res = {'response' : 'error', 'message' : 'This email is not registered', 'email' : email}
    return render_template('forgot-password.html', res=res)

@login.route('/verify-otp', methods=['POST'])
def verify_otp():
    otp = request.form.get('otp')
    email = request.form.get('email')
    origin = request.form.get('origin')
    id = is_user_exist(email)
    _, otps = get_otp_count(id)
    if otps and otp == otps[0]:
        res = {'otp' : True, 'response' : 'success', 'email' : email, 'origin':origin}

        if origin == 'forgot-password':
            res = {'response':'success', 'origin' : origin, 'email' : email}
            return render_template('update-password.html', res=res)

    else:
        res = {'otp' : False, 'response' : 'error', 'message' : 'Wrong OTP entered.', 'email' : email, 'origin':origin}
    return render_template('otp-verification.html', res=res)

@login.route('/update-password', methods=['POST'])
def update_password():
    email = request.form.get('email')
    origin = request.form.get('origin')
    password = request.form.get('password')
    if password and len(password)>7:
        id = is_user_exist(email)
        if id:
            change_password(id, password)
            res = {'response':'success', 'message':'Password successfully updated.'}
    return redirect(url_for('login.login_page', res=res))

@login.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('login.login_page'))