import psycopg2
from connect import get_connection
import json

def search(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def upsert(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_user(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def bulk_insert(users):
    conn = get_connection()
    cur = conn.cursor()
    users_json = json.dumps(users)
    cur.execute("CALL bulk_insert_users(%s::jsonb)", (users_json,))
    conn.commit()
    cur.close()
    conn.close()

def get_page(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_phonebook_page(%s, %s)", (limit, offset))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def delete_user(name=None, phone=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_user(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()