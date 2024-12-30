import pandas as pd
from mysql.connector import Error
import mysql.connector

def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Himani@2005",
            database="face_recognition_db"
        )
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

conn = connect_to_db()
# if not conn:
#     return [], []
        
# cursor = conn.cursor()
df=pd.DataFrame
# print(cursor.execute("SELECT count(*) FROM face_recognition_db.checkins  limit 3"))
# print(SELECT * FROM face_recognition_db.checkins limit 3;)
# print(cursor)
# conn.commit()
# cursor.execute("""INSERT INTO checkins (user_id, user_name, face_encoding)  VALUES (%s, %s, %s)
#                     """, (user_id, user_name, face_encoding_bytes))
cursor = conn.cursor()
sql = """SELECT * FROM face_recognition_db.checkins  limit 3"""
cursor.execute(sql)
# df=conn.commit()
df=cursor.fetchall()
print(df)
if conn and conn.is_connected():
    cursor.close()
    conn.close()