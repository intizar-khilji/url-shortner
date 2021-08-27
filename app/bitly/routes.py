from flask import redirect, url_for, render_template, request
from . import bitly, home_url
from .database import check_url_availablity, click_increment, encrypt, decrypt, get_user_details, get_users_links
from app import app_config, session

reserved_urls = ['home', 'encrypt', 'decrypt', 'links']

@bitly.route('/')
@bitly.route('/home')
def home():
    user_details = {}
    users_links = None
    if 'user' in session:
        user_details = get_user_details(session['user'])
    res = eval(request.args.get('res')) if request.args.get('res') else None
    return render_template('home.html', res=res, user_details=user_details, users_links=users_links)

@bitly.route('/encrypt', methods=["POST"])
def encrypt_url():
    res = None
    original_url = request.form.get('original_url')
    custom_url = request.form.get('custom_url')
    id = None if not 'user' in session else session['user']

    if original_url:
        if id:
            database_response = check_url_availablity(custom_url, id)
            if database_response or (custom_url in reserved_urls):
                res = {'response' : 'error', 'message': 'This custom URL is not available', 'url' : custom_url, 'original_url' : original_url}
            else:
                encrypted_url = 'http://'+app_config['app-host']+'/'+encrypt(original_url, id, custom_url)
                res = {'response' : 'success', 'encrypted_url':encrypted_url}
        else:
            encrypted_url = 'http://'+app_config['app-host']+'/'+encrypt(original_url, id)
            res = {'response' : 'success', 'encrypted_url':encrypted_url}
    return redirect(url_for(home_url, res=res))

@bitly.route('/links')
def links():
    user_details = None
    user_links = None
    if 'user' in session:
        user_details = get_user_details(session['user'])
        user_links = get_users_links(session['user'])
        # print(user_links)
    return render_template('links.html', user_details=user_details, user_links=user_links)

@bitly.route('/<encrypted_url>')
def decrypt_url(encrypted_url):
    original_url = decrypt(encrypted_url.strip(), id)
    flag = click_increment(encrypted_url)
    if original_url and flag:
        return redirect(original_url)
    return '<h1>404 not found</h>'

@bitly.route('/activity', methods=['POST'])
def activity():
    data = request.get_json()
    print(data)
    return redirect(url_for('.links'))