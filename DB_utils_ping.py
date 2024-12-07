import sys
import psycopg2
from tabulate import tabulate
from threading import Lock
from dotenv import load_dotenv
import os
from datetime import date


load_dotenv()
DB_NAME = "Listen"
DB_USER = "postgres"
DB_HOST = "127.0.0.1"
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')

cur = None
db = None
create_event_lock = Lock()


def db_connect():
    exit_code = 0
    # print(password)
    try:
        global db
        db = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, 
                              host=DB_HOST, port=DB_PORT)
        print("Successfully connect to DBMS.")
        global cur
        cur = db.cursor()
        return db

    except psycopg2.Error as err:
        print("DB error: ", err)
        exit_code = 1
    except Exception as err:
        print("Internal Error: ", err)
        raise err
    # finally:
    #     if db is not None:
    #         db.close()
    sys.exit(exit_code)


def print_table(cur):
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    return tabulate(rows, headers=columns, tablefmt="github")


# ============================= User Account =============================
def db_register_user(username, pwd, email):
    # fetch largest uid
    cmd = """
            SELECT MAX(user_id)
            FROM listener
            """
    # print(cur.mogrify(cmd, [username]))
    cur.execute(cmd, [email])
    max_uid = int(cur.fetchone()[0])
    cur_uid = max_uid + 1

    cur_date = date.today()


    cmd = """
            insert into "listener" (user_id, user_name, join_date, subscription_type, email, password, country, is_admin) 
            values (%s, %s, %s, 'F', %s, %s, 'Taiwan', false)
            RETURNING user_id;
            """
    cur.execute(cmd, [cur_uid, username, cur_date, email, pwd])

    userid = cur.fetchone()[0]
    db.commit()

    return userid

def fetch_user_by_email(email):
    cmd = """
            SELECT user_id, user_name, password, is_admin
            FROM listener
            WHERE email = %s;
            """
    # print(cur.mogrify(cmd, [username]))
    cur.execute(cmd, [email])
    data = cur.fetchall()[0]

    userid, username, pwd, is_admin = data
    return userid, username, pwd, is_admin

def user_name_exist(username):

    cmd = """
            select count(*) from "listener"
            where user_name = %s;
            """
    # print(cur.mogrify(cmd, [username]))
    cur.execute(cmd, [username])

    count = cur.fetchone()[0]
    return count > 0

def user_email_exist(email):

    cmd = """
            select count(*) from "listener"
            where email = %s;
            """
    # print(cur.mogrify(cmd, [email]))
    cur.execute(cmd, [email])

    count = cur.fetchone()[0]
    return count > 0

# ============================= Artist Account =============================

def db_register_artist(artistname, pwd, email):
    # fetch largest uid
    cmd = """
            SELECT MAX(artist_id)
            FROM artist
            """
    # print(cur.mogrify(cmd, [artistname]))
    cur.execute(cmd, [])
    max_uid = int(cur.fetchone()[0])
    cur_uid = max_uid + 1
    cur_date = date.today()

    cmd = """
            insert into "artist" (artist_id, artist_name, debut_date, email, password, bio) 
            values (%s, %s, %s, %s, %s, %s)
            RETURNING artist_id;
            """
    cur.execute(cmd, [cur_uid, artistname, cur_date, email, pwd, ''])

    artist_id = cur.fetchone()[0]
    db.commit()

    return artist_id

def fetch_artist_by_email(email):
    cmd = """
            SELECT artist_id, artist_name, password
            FROM artist
            WHERE email = %s;
            """
    # print(cur.mogrify(cmd, [artistname]))
    cur.execute(cmd, [email])
    data = cur.fetchall()[0]

    artistid, artistname, pwd, = data
    return artistid, artistname, pwd

def artist_name_exist(artistname):
    cmd = """
            select count(*) from "artist"
            where artist_name = %s;
            """
    # print(cur.mogrify(cmd, [artistname]))
    cur.execute(cmd, [artistname])

    count = cur.fetchone()[0]
    return count > 0

def artist_email_exist(email):
    cmd = """
            select count(*) from "artist"
            where email = %s;
            """
    # print(cur.mogrify(cmd, [email]))
    cur.execute(cmd, [email])

    count = cur.fetchone()[0]
    return count > 0

# ============================= Artist Operation =============================

def artist_album_exist(artist_id, album):
    cmd = """
            select count(*) from "album"
            where artist_id = %s and title = %s;
            """
    # print(cur.mogrify(cmd, [email]))
    cur.execute(cmd, [artist_id, album])

    count = cur.fetchone()[0]
    return count > 0

def db_register_album(artist_id, album, genre):
    # fetch largest uid
    cmd = """
            SELECT MAX(album_id)
            FROM album
            """
    # print(cur.mogrify(cmd, [artistname]))
    cur.execute(cmd, [])
    max_uid = int(cur.fetchone()[0])
    cur_uid = max_uid + 1
    cur_date = date.today()

    cmd = """
            insert into "album" (album_id, release_date, artist_id, title, genre, cover_image) 
            values (%s, %s, %s, %s, %s, %s)
            """
    cur.execute(cmd, [cur_uid, cur_date, artist_id, album, genre, 'test.png'])

    db.commit()

    return True
