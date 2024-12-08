from tabulate import tabulate
from global_db import get_global_db

def print_table(cur):
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    return tabulate(rows, headers=columns, tablefmt="github")


# ============================= System function =============================
def db_register_user(username, pwd, email):
    db, cur = get_global_db()
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
    db, cur = get_global_db()
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

    db, cur = get_global_db()
    cmd = """
            select count(*) from "USER"
            where User_name = %s;
            """
    # print(cur.mogrify(cmd, [username]))
    cur.execute(cmd, [username])

    count = cur.fetchone()[0]
    return count > 0

def userid_exist(userid):
    db, cur = get_global_db()
    cmd = """
            select count(*) 
            from "USER"
            where User_id = %s;
            """
    cur.execute(cmd, [userid])
    count = cur.fetchone()[0]
    return count > 0

def list_playlist(user_id):
    db, cur = get_global_db()
    query = """
            SELECT *
            FROM Playlist
            WHERE Listener_id = %s;
            """
    cur.execute(query, [user_id])

    return print_table(cur)

def list_song_from_playlist(playlist_name):
    
    db, cur = get_global_db()
    query = f"""
            SELECT 
                pl.title as playlist_title,
                s.title as song_title, 
                a.name as artist_name,
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
    
    db, cur = get_global_db()
    print(db)
    print(cur)
    query = f"""
            SELECT s.title, s.language, s.genre, s.likes, a.artist_name
            FROM song as s
            Join artist as a on s.artist_id = a.artist_id
            WHERE s.title LIKE '%{song_name}%';
            """
    # print(cur.mogrify(query))
    cur.execute(query)

    return print_table(cur)

def query_album(album_name):
    db, cur = get_global_db()
    
    query = f"""
            SELECT alb.title, alb.genre, a.name
            FROM album as alb
            Join artist as a on a.artist_id = alb.artist_id
            WHERE alb.title LIKE '%{album_name}%';
            """
    # print(cur.mogrify(query))
    cur.execute(query)

    return print_table(cur)

def query_artist(artist_name):
    db, cur = get_global_db()
    
    query = f"""
            SELECT *
            FROM artist as a
            WHERE a.name LIKE '%{artist_name}%';
            """
    # print(cur.mogrify(query))
    cur.execute(query)

    return print_table(cur)

def create_playlist(user_id, playlist_title, playlist_description, public_or_not, commit=True):
    db, cur = get_global_db()
    ## playlist_id 要拿掉
    query = f"""
            INSERT INTO PLAYLIST (listener_id, title, creation_date, description, is_public)
            Values({user_id}, '{playlist_title}', CURRENT_DATE, '{playlist_description}', '{public_or_not}')
            RETURNING Playlist_id;
            """
    # print(cur.mogrify(query))
    cur.execute(query)
    print(f'After exec')
    playlist_id = cur.fetchone()[0]
    if commit:
        db.commit()
    return playlist_id

def add_song_to_playlist(user_id, playlist_id, song_id, commit=True):
    db, cur = get_global_db()
    ## playlist_id 要拿掉
    query = f"""
            INSERT INTO playlist_contain (playlist_id, song_id)
            SELECT {playlist_id}, {song_id}
            WHERE EXISTS (
                SELECT 1
                FROM playlist
                WHERE playlist.playlist_id = {playlist_id}
                AND playlist.listener_id = {user_id}
            )
            RETURNING playlist_id;
            """
    # print(cur.mogrify(query))
    cur.execute(query)
    print(f'After exec')
    playlist_id = cur.fetchone()[0]
    if commit:
        db.commit()
    return playlist_id

def delete_song_from_playlist(user_id, playlist_id, song_id):
    db, cur = get_global_db()
    query =f"""
            DELETE FROM playlist_contain
            WHERE playlist_id = {playlist_id}
            AND song_id = {song_id}
            AND EXISTS (
                SELECT 1
                FROM playlist
                WHERE playlist.playlist_id = playlist_contain.playlist_id
                AND playlist.listener_id = {user_id}
            );
            """
    
    cur.execute(query)
    db.commit()