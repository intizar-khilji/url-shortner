from mysql.connector import connect
from app import database_config
import hashlib, random

def create_new_user(name, email, password):
    password = hashlib.sha256(password.encode()).hexdigest()
    print(email, name, password)
    res = False
    try:
        conn = connect(host=database_config['host'], user=database_config['user'], password=database_config['password'], database=database_config['database-name'])
        cur = conn.cursor()
        cur.execute(f"insert into users (name, email, password) values ('{name}','{email}','{password}')")
        res = True
    except:
        conn.rollback()
    finally:
        conn.commit()
        conn.close()
    return res

def is_user_exist(email):
    res = 0
    try:
        conn = connect(host=database_config['host'], user=database_config['user'], password=database_config['password'], database=database_config['database-name'])
        cur = conn.cursor()
        cur.execute(f"select id from users where email='{email}'")
        id, = cur.fetchall()[0]
        if id:
            res = id
    except:
        conn.rollback()
    finally:
        conn.commit()
        conn.close()
    return res

def authenticate_user(email, password):
    res = 0
    try:
        conn = connect(host=database_config['host'], user=database_config['user'], password=database_config['password'], database=database_config['database-name'])
        cur = conn.cursor()
        cur.execute(f"select id, password from users where email='{email}'")
        database_res = cur.fetchall()[0]
        id = database_res[0]
        password_from_database = database_res[1]
        password = hashlib.sha256(password.encode()).hexdigest()
        if password_from_database == password:
            res = id
    except:
        conn.rollback()
    finally:
        conn.commit()
        conn.close()
    return res

def generate_otp(id):
    otp = ''.join([random.choice('0123456789') for _ in range(6)])
    try:
        conn = connect(host=database_config['host'], user=database_config['user'], password=database_config['password'], database=database_config['database-name'])
        cur = conn.cursor()
        cur.execute("insert into otp (id, otp) values({}, '{}')".format(id, otp))
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.commit()
        conn.close()
    return otp

def get_otp_count(id):
    count = 0
    otps = None
    try:
        conn = connect(host=database_config['host'], user=database_config['user'], password=database_config['password'], database=database_config['database-name'])
        cur = conn.cursor()
        cur.execute("delete from otp where time <= date_sub(now(), interval 10 minute)")
        cur.execute("select otp from otp where id={} order by time desc".format(id))
        otps = cur.fetchall()
        otps = [i for i, in otps]
        count = len(otps)
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.commit()
        conn.close()
    return count, otps

def change_password(id,password):
    password = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn = connect(host=database_config['host'], user=database_config['user'], password=database_config['password'], database=database_config['database-name'])
        cur = conn.cursor()
        cur.execute(f"update users set password='{password}' where id='{id}'")
    except:
        conn.rollback()
    finally:
        conn.commit()
        conn.close()

