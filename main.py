import cv2
import face_recognition
import numpy as np
import mysql.connector
from datetime import datetime
from mysql.connector import Error

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

def fetch_known_faces():
    try:
        conn = connect_to_db()
        if not conn:
            return [], []
        
        cursor = conn.cursor()
        cursor.execute("SELECT face_encoding, user_name FROM checkins")
        
        known_face_encodings = []
        known_face_names = []
        
        for encoding_blob, name in cursor.fetchall():
            face_encoding = np.frombuffer(encoding_blob, dtype=np.float64)
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)
            
        return known_face_encodings, known_face_names
    except Error as e:
        print(f"Error fetching faces: {e}")
        return [], []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def add_checkin(user_id, user_name, face_encoding):
    try:
        conn = connect_to_db()
        if not conn:
            return False
            
        cursor = conn.cursor()
        sql = """INSERT INTO checkins 
                (user_id, user_name, checkin_time, face_encoding) 
                VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (user_id, user_name, datetime.now(), face_encoding))
        conn.commit()
        return True
    except Error as e:
        print(f"Error adding check-in: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def recognize_face():
    known_face_encodings, known_face_names = fetch_known_faces()
    if not known_face_encodings:
        print("No registered faces found in database")
        return

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Failed to open webcam")
        return

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            
            if True in matches:
                best_match_index = np.argmin(face_distances)
                name = known_face_names[best_match_index]
                
                if add_checkin(1, name, face_encoding.tobytes()):
                    color = (0, 255, 0)  
                    cv2.putText(frame, f"Welcome {name}", (left + 6, bottom + 23),
                              cv2.FONT_HERSHEY_DUPLEX, 0.6, color, 1)
            else:
                color = (0, 0, 255)  
                cv2.putText(frame, "Unknown", (left + 6, bottom + 23),
                          cv2.FONT_HERSHEY_DUPLEX, 0.6, color, 1)

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_face()