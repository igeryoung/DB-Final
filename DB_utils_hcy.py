import sys
import psycopg2
from tabulate import tabulate
from threading import Lock
from dotenv import load_dotenv
import os

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


# ============================= System function =============================
def db_register_user(username, pwd, email):
    cmd = """
            insert into "USER" (User_name, Password, Email) values (%s, %s, %s)
            RETURNING User_id;
            """
    cur.execute(cmd, [username, pwd, email])
    userid = cur.fetchone()[0]

    cmd = """
            insert into "USER_ROLE" (User_id, Role) VALUES (%s, 'User');
            """
    cur.execute(cmd, [userid])
    db.commit()

    return userid


def fetch_user(userid):
    cmd = """
            select * 
            from "USER" u
            join "USER_ROLE" r on u.User_id = r.User_id
            where u.User_id = %s;
            """
    cur.execute(cmd, [userid])

    rows = cur.fetchall()
    if not rows:
        return None, None, None, None, None
    else:
        isUser = False
        isAdmin = False
        for row in rows:
            userid, username, pwd, email, userid, role = row

            if role == "User":
                isUser = True
            elif role == "Admin":
                isAdmin = True

    return username, pwd, email, isUser, isAdmin


def username_exist(username):

    cmd = """
            select count(*) from "USER"
            where User_name = %s;
            """
    # print(cur.mogrify(cmd, [username]))
    cur.execute(cmd, [username])

    count = cur.fetchone()[0]
    return count > 0


def userid_exist(userid):
    cmd = """
            select count(*) 
            from "USER"
            where User_id = %s;
            """
    cur.execute(cmd, [userid])
    count = cur.fetchone()[0]
    return count > 0


def list_playlist(user_id):
    query = """
            SELECT *
            FROM Playlist
            WHERE Listener_id = %s;
            """
    cur.execute(query, [user_id])

    return print_table(cur)


def list_song_from_playlist(playlist_name):
    
    query = f"""
            SELECT 
                s.title, 
                a.name,
                s.language, 
                s.genre
            FROM 
                Song AS s
            JOIN 
                Playlist_contain AS p ON s.song_id = p.song_id
            JOIN 
                Playlist AS pl ON p.playlist_id = pl.playlist_id
            JOIN 
                Artist AS a ON s.artist_id = a.artist_id
            WHERE 
                pl.title LIKE '%{playlist_name}%';
            """
    # print(cur.mogrify(query))
    cur.execute(query)

    return print_table(cur)

def query_song(song_name):
    
    query = f"""
            SELECT * 
            FROM song as s
            WHERE s.title LIKE '%{song_name}%';;
            """
    # print(cur.mogrify(query))
    cur.execute(query)

    return print_table(cur)