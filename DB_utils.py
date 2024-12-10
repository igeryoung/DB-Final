from tabulate import tabulate
from datetime import date
from global_db import get_global_db

def print_table(cur):
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    return tabulate(rows, headers=columns, tablefmt="github")


# ============================= User Account =============================
def db_register_user(username, pwd, email):
    db, cur = get_global_db()
    

    cmd = """
            insert into "listener" (listener_name, join_date, subscription_type, email, password, country, is_admin) 
            values (%s, CURRENT_DATE, 'F', %s, %s, 'Taiwan', false)
            RETURNING listener_id;
            """
    cur.execute(cmd, [username, email, pwd])

    userid = cur.fetchone()[0]
    db.commit()

    return userid

def fetch_user_by_email(email):
    db, cur = get_global_db()

    cmd = f"""
            SELECT listener_id, listener_name, password, is_admin
            FROM listener
            WHERE email = '{email}';
            """
    # print(cur.mogrify(cmd, [username]))
    cur.execute(cmd)
    data = cur.fetchone()

    return data

def user_name_exist(username):
    db, cur = get_global_db()

    cmd = """
            select count(*) from "listener"
            where listener_name = %s;
            """
    # print(cur.mogrify(cmd, [username]))
    cur.execute(cmd, [username])

    count = cur.fetchone()[0]
    return count > 0

def user_email_exist(email):
    db, cur = get_global_db()

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
    db, cur = get_global_db()
    # fetch largest uid
    cmd = """
            SELECT MAX(artist_id)
            FROM artist
            """
    
    cmd = """
            insert into "artist" (artist_name, debut_date, email, password, bio) 
            values (%s, CURRENT_DATE, %s, %s, %s)
            RETURNING artist_id;
            """
    cur.execute(cmd, [artistname, email, pwd, ''])

    artist_id = cur.fetchone()[0]
    db.commit()

    return artist_id

def fetch_artist_by_email(email):
    db, cur = get_global_db()
    cmd = f"""
            SELECT artist_id, artist_name, password
            FROM artist
            WHERE email = '{email}';
            """
    # print(cur.mogrify(cmd, [artistname]))
    cur.execute(cmd)
    data = cur.fetchone()
    return data

def artist_name_exist(artistname):
    db, cur = get_global_db()
    cmd = """
            select count(*) from "artist"
            where artist_name = %s;
            """
    # print(cur.mogrify(cmd, [artistname]))
    cur.execute(cmd, [artistname])

    count = cur.fetchone()[0]
    return count > 0

def artist_email_exist(email):
    db, cur = get_global_db()
    cmd = """
            select count(*) from "artist"
            where email = %s;
            """
    # print(cur.mogrify(cmd, [email]))
    cur.execute(cmd, [email])

    count = cur.fetchone()[0]
    return count > 0

def query_artist_id_by_name(name):
    db, cur = get_global_db()
    query = """
        SELECT artist_id FROM artist
        WHERE artist_name = %s;
    """
    
    cur.execute(query, [name])
    result = cur.fetchone()
    
    if result:
        return result[0]
    else:
        return -1 

# ============================= Album Operation =============================

def artist_album_exist(artist_id, album):
    db, cur = get_global_db()
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
    db, cur = get_global_db()
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

def list_artist_album(artist_id):
    db, cur = get_global_db()
    query = """
            SELECT release_date, title, genre, cover_image
            FROM album
            WHERE artist_id = %s;
            """
    cur.execute(query, [artist_id])

    return print_table(cur)

def query_album_id_by_title_and_artist(artist_id, title):
    db, cur = get_global_db()
    cmd = """
            SELECT album_id FROM "album"
            WHERE artist_id = %s AND title = %s;
          """
    cur.execute(cmd, [artist_id, title])
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return -1

def query_song_in_album(artist_id, album_title):
    db, cur = get_global_db()

    if album_title == "All":
        cmd = """
                SELECT album_id FROM "album"
                WHERE title = %s;
            """
        cur.execute(cmd, [artist_id, album_title])
        result = cur.fetchone()
        
        if result:
            album_id = result[0]
            # print('id: ', album_id)
            cmd = """
                SELECT song_id, title FROM "song"
                WHERE album_id = %s
            """
            cur.execute(cmd, [int(album_id)])
            return print_table(cur)

        else:
            return -1

    else:
        cmd = """
                SELECT album_id FROM "album"
                WHERE artist_id = %s AND title = %s;
            """
        cur.execute(cmd, [artist_id, album_title])
        result = cur.fetchone()
        
        if result:
            album_id = result[0]
            # print('id: ', album_id)
            cmd = """
                SELECT song_id, title FROM "song"
                WHERE album_id = %s
            """
            cur.execute(cmd, [int(album_id)])
            return print_table(cur)

        else:
            return -1

def delete_album(album_id, recur):
    db, cur = get_global_db()
    
    if recur == "N":
        update_query = """
            UPDATE song
            SET album_id = 1
            WHERE album_id = %s;
        """
        cur.execute(update_query, [album_id])  # Use %s and provide the parameter as a list

        print("Update complete")

        # Delete the album
        delete_query = """
            DELETE FROM album
            WHERE album_id = %s;
        """
        cur.execute(delete_query, [album_id])  # Use %s and provide the parameter as a list

        # Commit the transaction
        db.commit()
    else:
        query =f"""
                DELETE FROM song
                WHERE album_id = {album_id};
                """
        cur.execute(query)

        print("clear song")

        query =f"""
                DELETE FROM album
                WHERE album_id = {album_id};
                """
        
        cur.execute(query)
        db.commit()
    return

def user_query_song_in_album(album_title):
    db, cur = get_global_db()

    cmd = f"""
            SELECT album_id FROM "album"
            WHERE title = '{album_title}';
        """
    cur.execute(cmd)
    result = cur.fetchone()

    print(result)
    
    if result:
        album_id = result[0]
        # print('id: ', album_id)
        cmd = """
            SELECT song_id, title FROM "song"
            WHERE album_id = %s
        """
        cur.execute(cmd, [int(album_id)])
        return print_table(cur)

    else:
        return -1

# ============================= Song Operation =============================

def db_register_song(artist_id, title, genre, language, duration=60, album=None):
    db, cur = get_global_db()
    album_id = -1
    if album:
        album_id = query_album_id_by_title_and_artist(artist_id, album)
    
    if album_id != -1:
        cmd = """
                insert into "song" (likes,played_times,artist_id,album_id,duration,release_date,title,genre,audio_file,language) 
                values (0, 0, %s, %s, %s, CURRENT_DATE, %s, %s, %s, %s)
                """
        cur.execute(cmd, [int(artist_id), int(album_id), int(duration), title, genre, 'test.mp3', language])
    else:
        cmd = """
                insert into "song" (likes,played_times,artist_id,duration,release_date,title,genre,audio_file,language) 
                values (0, 0, %s,  %s, CURRENT_DATE, %s, %s, %s, %s)
                """
        cur.execute(cmd, [int(artist_id), int(duration), title, genre, 'test.mp3', language])
        
    db.commit()

    return True

def list_artist_song(artist_id):
    db, cur = get_global_db()
    query = """
            SELECT release_date, title, duration, genre, language, likes, played_times
            FROM song
            WHERE artist_id = %s;
            """
    cur.execute(query, [int(artist_id)])

    return print_table(cur)

def query_song_id_by_artist_id_and_title(artist_id, title):
    db, cur = get_global_db()
    cmd = """
            SELECT song_id FROM "song"
            WHERE artist_id = %s AND title = %s;
          """
    cur.execute(cmd, [artist_id, title])
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return -1

def delete_song_from_playlist(song_id):
    db, cur = get_global_db()
    query =f"""
            DELETE FROM listen_history
            WHERE song_id = {song_id};
            """
    cur.execute(query)

    query =f"""
            DELETE FROM playlist_contain
            WHERE song_id = {song_id};
            """
    cur.execute(query)

    query =f"""
            DELETE FROM song
            WHERE song_id = {song_id};
            """
    cur.execute(query)

    db.commit()

def query_song_id_by_song_title(title):
    db, cur = get_global_db()
    cmd = """
            SELECT song_id FROM song
            WHERE title = %s;
          """
    cur.execute(cmd, [title])
    result = cur.fetchone()
    
    if result:
        return result[0]
    else:
        return -1

def play_song(listener_id, song_id):
    db, cur = get_global_db()
    
    print(listener_id, song_id)
    # Step 1: Add 1 record to listen_history
    add_history_cmd = """
        INSERT INTO listen_history (listener_id, song_id, listen_time)
        VALUES (%s, %s, NOW());
    """
    cur.execute(add_history_cmd, [int(listener_id), int(song_id)])
    
    # Step 2: Increment the played_times for the song
    increment_played_times_cmd = """
        UPDATE song
        SET played_times = played_times + 1
        WHERE song_id = %s;
    """
    cur.execute(increment_played_times_cmd, [song_id])
    
    db.commit()
    return

def like_song_by_song_id(song_id):
    db, cur = get_global_db()
    
    increment_likes_cmd = """
        UPDATE song
        SET likes = likes + 1
        WHERE song_id = %s;
    """
    cur.execute(increment_likes_cmd, [song_id])
    
    db.commit()
    return f"Song ID {song_id} liked successfully."

# ============================= Cash Operation =============================

def deposit_cash(listener_id, value):
    db, cur = get_global_db()
    deposit_query = """
        UPDATE listener
        SET cash = cash + %s
        WHERE listener_id = %s;
    """
    cur.execute(deposit_query, [int(value), listener_id])
    db.commit()

def query_cash(listener_id):
    db, cur = get_global_db()
    deposit_query = """
        SELECT cash
        From listener
        WHERE listener_id = %s;
    """
    cur.execute(deposit_query, [int(listener_id)])
    result = cur.fetchone()
    return result[0]

def donate_cash(listener_id, artist_id, value):
    db, cur = get_global_db()

    try:
        deduct_user_cash_query = """
            UPDATE listener
            SET cash = cash - %s
            WHERE listener_id = %s;
        """
        cur.execute(deduct_user_cash_query, [value, listener_id])

        # Insert donation record
        insert_donation_query = """
            INSERT INTO donation (listener_id, artist_id, amount)
            VALUES (%s, %s, %s);
        """
        cur.execute(insert_donation_query, [listener_id, artist_id, value])

        # Add cash to artist
        update_artist_cash_query = """
            UPDATE artist
            SET cash = cash + %s
            WHERE artist_id = %s;
        """
        cur.execute(update_artist_cash_query, [value, artist_id])

        # Commit transaction
        db.commit()
        return

    except Exception as e:
        db.rollback()
        return f"An error occurred: {e}"
    
def artist_query_cash(listener_id):
    db, cur = get_global_db()
    deposit_query = """
        SELECT cash
        From artist
        WHERE artist_id = %s;
    """
    cur.execute(deposit_query, [int(listener_id)])
    result = cur.fetchone()
    return result[0]

# ============================= Follow Operation =============================

def follow_artist(listener_id, artist_id, name):
    db, cur = get_global_db()

    try:
        # Check if the user already follows the artist
        check_follow_query = """
            SELECT 1 FROM follow
            WHERE listener_id = %s AND artist_id = %s;
        """
        cur.execute(check_follow_query, [listener_id, artist_id])
        result = cur.fetchone()

        if result:
            return "You are already following this artist."

        # Insert follow record
        insert_follow_query = """
            INSERT INTO follow (listener_id, artist_id)
            VALUES (%s, %s);
        """
        cur.execute(insert_follow_query, [listener_id, artist_id])

        # Update artist's follow_num
        update_artist_follow_query = """
            UPDATE artist
            SET follow_num = follow_num + 1
            WHERE artist_id = %s;
        """
        cur.execute(update_artist_follow_query, [artist_id])

        # Commit the transaction
        db.commit()
        return f"You are now following Artist [{name}]."

    except Exception as e:
        db.rollback()
        return f"An error occurred: {e}"

def unfollow_artist(listener_id, artist_id, name):
    db, cur = get_global_db()

    try:
        # Check if the follow record exists
        check_follow_query = """
            SELECT 1 FROM follow
            WHERE listener_id = %s AND artist_id = %s;
        """
        cur.execute(check_follow_query, [listener_id, artist_id])
        result = cur.fetchone()

        if not result:
            return "You are not following this artist."

        # Delete the follow record
        delete_follow_query = """
            DELETE FROM follow
            WHERE listener_id = %s AND artist_id = %s;
        """
        cur.execute(delete_follow_query, [listener_id, artist_id])

        # Update artist's follow_num
        update_artist_follow_query = """
            UPDATE artist
            SET follow_num = follow_num - 1
            WHERE artist_id = %s AND follow_num > 0;
        """
        cur.execute(update_artist_follow_query, [artist_id])

        # Commit the transaction
        db.commit()
        return f"You are now unfollowed Artist [{name}]."

    except Exception as e:
        db.rollback()
        return f"An error occurred: {e}"

def list_all_follow_artist(listener_id):
    db, cur = get_global_db()

    try:
        # Query to get all followed artists with required details
        query = """
            SELECT 
                a.artist_name, 
                a.total_played, 
                a.follow_num, 
                a.bio
            FROM follow f
            JOIN artist a ON f.artist_id = a.artist_id
            WHERE f.listener_id = %s
            ORDER BY a.artist_name;
        """
        
        cur.execute(query, [listener_id])
        return print_table(cur)
    
    except Exception as e:
        return f"An error occurred: {e}"
    
def artist_query_follow_num(listener_id):
    db, cur = get_global_db()
    deposit_query = """
        SELECT follow_num
        From artist
        WHERE artist_id = %s;
    """
    cur.execute(deposit_query, [int(listener_id)])
    result = cur.fetchone()
    return result[0]

def list_playlist(listener_id):
    db, cur = get_global_db()

    if listener_id == 'All':
        query = """
                SELECT *
                FROM Playlist
                """
        cur.execute(query, [])
    else:
        query = """
                SELECT *
                FROM Playlist
                WHERE Listener_id = %s;
                """
        cur.execute(query, [listener_id])

    return print_table(cur)

def list_song_from_playlist(playlist_name):
    
    db, cur = get_global_db()
    query = f"""
            SELECT 
                pl.title as playlist_title,
                s.title as song_title, 
                a.artist_name as artist_name,
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
                pl.title LIKE '%{playlist_name}%'
            AND 
	            pl.is_public = 'Y';
            """
    # print(cur.mogrify(query))
    cur.execute(query)

    return print_table(cur)

def query_song(song_name):
    
    db, cur = get_global_db()
    print(db)
    print(cur)
    query = f"""
            SELECT s.song_id, s.title, s.language, s.genre, s.likes, a.artist_name
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
            SELECT alb.title, alb.genre, a.artist_name
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
            WHERE a.artist_name LIKE '%{artist_name}%';
            """
    # print(cur.mogrify(query))
    cur.execute(query)

    return print_table(cur)

def create_playlist(listener_id, playlist_title, playlist_description, public_or_not, commit=True):
    db, cur = get_global_db()
    ## playlist_id 要拿掉
    query = f"""
            INSERT INTO PLAYLIST (listener_id, title, creation_date, description, is_public)
            Values({listener_id}, '{playlist_title}', CURRENT_DATE, '{playlist_description}', '{public_or_not}')
            RETURNING Playlist_id;
            """
    # print(cur.mogrify(query))
    cur.execute(query)
    print(f'After exec')
    playlist_id = cur.fetchone()[0]
    if commit:
        db.commit()
    return playlist_id

def add_song_to_playlist(listener_id, playlist_id, song_id, commit=True):
    db, cur = get_global_db()
    
    query = f"""
            INSERT INTO playlist_contain (playlist_id, song_id)
            SELECT {playlist_id}, {song_id}
            WHERE EXISTS (
                SELECT 1
                FROM playlist
                WHERE playlist.playlist_id = {playlist_id}
                AND playlist.listener_id = {listener_id}
            )
            RETURNING playlist_id;
            """
    # print(cur.mogrify(query))
    cur.execute(query)
    print(f'After exec')
    return_playlist_id = cur.fetchone()[0]
    
    if commit:
        db.commit()
    return return_playlist_id

def delete_song_from_playlist(listener_id, playlist_id, song_id, commit=True):
    db, cur = get_global_db()
    query =f"""
            DELETE FROM playlist_contain
            WHERE playlist_id = {playlist_id}
            AND song_id = {song_id}
            AND EXISTS (
                SELECT 1
                FROM playlist
                WHERE playlist.playlist_id = playlist_contain.playlist_id
                AND playlist.listener_id = {listener_id}
            );
            """
    
    cur.execute(query)
    if commit:
        db.commit()
    return
       
def list_user_history(listener_id):
    db, cur = get_global_db()
    if(listener_id == "All"):
        query = """
                SELECT *
                FROM listen_history
                ORDER BY listener_id ASC, song_id ASC, listen_time ASC;
                """
        cur.execute(query)
    else:
        query = f"""
                SELECT *
                FROM listen_history
                WHERE listener_id = {listener_id}
                ORDER BY listener_id ASC, song_id ASC, listen_time ASC;
                """
        cur.execute(query)

    return print_table(cur)

def list_user_playlist(listener_id):
    db, cur = get_global_db()
    if(listener_id == "All"):
        print("All")
        query = """
                SELECT * FROM public.playlist
                ORDER BY playlist_id ASC 
                """
        cur.execute(query)
    else:
        query = """
                SELECT * FROM public.playlist
                WHERE listener_id = %s
                ORDER BY playlist_id ASC 
                """
        cur.execute(query, [listener_id])

    return print_table(cur)

# ============================= Activity Operation =============================

def artist_activity_exist(listener_id, activity_title):
    db, cur = get_global_db()
    query = """
        SELECT 1 FROM artist_activity 
        WHERE artist_id = %s AND title = %s;
    """
    cur.execute(query, [listener_id, activity_title])
    return cur.fetchone() is not None

def db_register_activity(listener_id, title, description, location, event_date):
    db, cur = get_global_db()
    try:
        query = """
            INSERT INTO artist_activity (artist_id, title, description, location, event_date)
            VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(query, [listener_id, title, description, location, event_date])
        db.commit()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        db.rollback()
        return False
    
def artist_query_activity(listener_id):
    db, cur = get_global_db()

    # Query to fetch activities for the logged-in artist
    query = f"""
        SELECT title, description, location, event_date, created_at
        FROM artist_activity
        WHERE artist_id = {listener_id}
        ORDER BY event_date DESC;
    """

    cur.execute(query)
    return print_table(cur)

def query_activity_id_by_artist_id_and_title(artist_id, title):
    db, cur = get_global_db()
    query = """
        SELECT activity_id FROM artist_activity
        WHERE artist_id = %s AND title = %s;
    """
    cur.execute(query, [artist_id, title])
    result = cur.fetchone()
    return result[0] if result else -1

def delete_activity_by_id(activity_id):
    db, cur = get_global_db()
    try:
        query = """
            DELETE FROM artist_activity
            WHERE activity_id = %s;
        """
        cur.execute(query, [activity_id])
        db.commit()
    except Exception as e:
        print(f"Database error: {e}")
        db.rollback()

def user_query_activity(recent_date):
    db, cur = get_global_db()

    query = """
            SELECT title, description, location, event_date, created_at
            FROM artist_activity
            WHERE event_date <= %s
            ORDER BY event_date ASC;
        """
    cur.execute(query, [recent_date])
    return print_table(cur)

# ============================= Admin Operation =============================

def list_listener(uid):
    db, cur = get_global_db()
    if uid == "All":
        # Query to fetch all listener information
        query = """
            SELECT *
            FROM listener
            ORDER BY listener_id ASC
            FOR SHARE NOWAIT;
        """
        cur.execute(query)
    else:
        # Query to fetch all listener information
        query = f"""
            SELECT *
            FROM listener
            WHERE listener_id = '{int(uid)}'
            ORDER BY listener_id ASC;
        """
        cur.execute(query)
    return print_table(cur)

def list_artist(uid):
    db, cur = get_global_db()
    print(uid)
    if uid == "All":
        query = """
            SELECT *
            FROM artist
            ORDER BY artist_id ASC
            FOR SHARE NOWAIT;
        """
        cur.execute(query)
    else:
        # Query to fetch all artist information
        query = f"""
            SELECT *
            FROM artist
            WHERE artist_id = '{int(uid)}'
            ORDER BY artist_id ASC;
        """
        cur.execute(query)
    return print_table(cur)

def check_listener_exists(listener_id):
        """Check if the listener exists in the database."""
        db, cur = get_global_db()
        query = """
            SELECT 1
            FROM listener
            WHERE listener_id = %s;
        """
        cur.execute(query, [listener_id])
        result = cur.fetchone()
        return result is not None

def delete_listener_by_id(listener_id):
    """Delete listener from the database."""
    db, cur = get_global_db()
    query = """
        DELETE FROM listener
        WHERE listener_id = %s;
    """
    cur.execute(query, [listener_id])
    db.commit()

    # Optionally, handle cascading deletions if necessary (e.g., playlists, follow relations, etc.)
    # Delete associated playlists
    delete_playlists_query = """
        DELETE FROM playlist
        WHERE listener_id = %s;
    """
    cur.execute(delete_playlists_query, [listener_id])

    # Delete associated follow relationships
    delete_follow_query = """
        DELETE FROM follow
        WHERE listener_id = %s;
    """
    cur.execute(delete_follow_query, [listener_id])

    db.commit()

def check_artist_exists(listener_id):
    """Check if the artist exists in the database."""
    db, cur = get_global_db()
    query = """
        SELECT 1
        FROM artist
        WHERE artist_id = %s;
    """
    cur.execute(query, [listener_id])
    result = cur.fetchone()
    return result is not None

def delete_artist_by_id(listener_id):
    """Delete artist and associated data from the database."""
    db, cur = get_global_db()
    
    # Delete songs by the artist
    delete_songs_query = """
        DELETE FROM song
        WHERE artist_id = %s;
    """
    cur.execute(delete_songs_query, [listener_id])
    
    # Delete albums by the artist
    delete_albums_query = """
        DELETE FROM album
        WHERE artist_id = %s;
    """
    cur.execute(delete_albums_query, [listener_id])
    
    # Delete artist activities
    delete_activities_query = """
        DELETE FROM artist_activity
        WHERE artist_id = %s;
    """
    cur.execute(delete_activities_query, [listener_id])
    
    # Delete follow relationships for the artist
    delete_follows_query = """
        DELETE FROM follow
        WHERE artist_id = %s;
    """
    cur.execute(delete_follows_query, [listener_id])
    
    # Finally, delete the artist from the artist table
    delete_artist_query = """
        DELETE FROM artist
        WHERE artist_id = %s;
    """
    cur.execute(delete_artist_query, [listener_id])
    
    # Commit all changes
    db.commit()

def list_user_donation(uid):
    db, cur = get_global_db()
    print(uid)
    if uid == "All":
        query = """
            SELECT *
            FROM donation
            ORDER BY donation_time ASC
            FOR SHARE NOWAIT;
        """
        cur.execute(query)
    else:
        # Query to fetch all donation information
        query = f"""
            SELECT *
            FROM donation
            WHERE listener_id = '{int(uid)}'
            ORDER BY donation_time ASC;
        """
        cur.execute(query)
    return print_table(cur)

