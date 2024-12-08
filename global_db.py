import sys
import psycopg2
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

def get_global_db():
    return db, cur