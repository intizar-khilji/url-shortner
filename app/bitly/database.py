from mysql.connector import connect
from app import database_config
from random import choice, randint
import string

def check_url_availablity(url, user=None):
    conn = connect(host=database_config['host'], user=database_config['user'], password=database_config['password'], database=database_config['database-name'])
    cur = conn.cursor()
    query = "select * from {} where encrypted_url='{}'".format('guests' if not user else 'users_links', url)
    cur.execute(query)
    database_response = cur.fetchall()
    conn.commit()
    conn.close()
    return database_response

def encrypt(original_url, user=None, custom=None):
    if custom:
        encrypted_url = custom
    try:
        conn = connect(host=database_config['host'], user=database_config['user'], password=database_config['password'], database=database_config['database-name'])
        cur = conn.cursor()
        while True and not custom:
            encrypted_url = ''.join([choice(string.ascii_letters+string.digits) for i in range(randint(6,10))])
            database_response = check_url_availablity(encrypted_url, user)
            if not database_response:
                break
        if not (original_url.startswith('http://') or original_url.startswith('https://')):
            original_url = 'http://'+original_url
        if not user:
            query = "insert into guests values('{}', '{}')".format(original_url, encrypted_url)
        else:
            query = "insert into users_links (id, original_url, encrypted_url, name) values({0}, '{1}', '{2}', (select name from users where id={0}))".format(user, original_url, encrypted_url)
        cur.execute(query)
    except Exception as e:
        print('error',e)
        conn.rollback()
    finally:
        conn.commit()
        conn.close()
    return encrypted_url

def decrypt(encrypted_url, user=None):
    conn = connect(host='localhost', user='root', password='', database='bitly')
    cur = conn.cursor()
    query = "select original_url from {} where encrypted_url='{}'".format('guests' if not user else 'users_links', encrypted_url)
    cur.execute(query)
    original_url = cur.fetchone()
    return original_url[0] if original_url else ''

def get_user_details(id):
    user_details = {}
    try:
        conn = connect(host=database_config['host'], user=database_config['user'], password=database_config['password'], database=database_config['database-name'])
        cur = conn.cursor()
        query = f"select email, name, activated, verified from users where id='{id}'"
        cur.execute(query)
        cols = ('email', 'name', 'activated', 'verified')
        data = cur.fetchone()
        i=0
        while i<len(cols):
            user_details[cols[i]] = data[i]
            i+=1
    except Exception as e:
        print('error',e)
        conn.rollback()
    finally:
        conn.commit()
        conn.close()
    return user_details

def get_users_links(id, page=1):
    conn = connect(host=database_config['host'], user=database_config['user'], password=database_config['password'], database=database_config['database-name'])
    cur = conn.cursor()
    query = "select original_url, encrypted_url, clicks, date(time) as `time`, isactive from users_links where id={} order by time desc".format(id)
    cur.execute(query)
    user_links = cur.fetchall()
    conn.commit()
    conn.close()
    return user_links

def click_increment(encrypted_url):
    flag = False
    try:
        conn = connect(host=database_config['host'], user=database_config['user'], password=database_config['password'], database=database_config['database-name'])
        cur = conn.cursor()
        query = "select clicks from users_links where encrypted_url='{}'".format(encrypted_url)
        cur.execute(query)
        current_clicks = cur.fetchall()
        if current_clicks:
            flag = True
            current_clicks = current_clicks[0][0]
            query = "update users_links set clicks={} where encrypted_url='{}'".format(current_clicks+1, encrypted_url)
            cur.execute(query)
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.commit()
        conn.close()
    return flag