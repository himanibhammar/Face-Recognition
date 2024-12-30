import face_recognition
import cv2
import numpy as np
import mysql.connector
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

def register_user():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Failed to open webcam")
        return

    user_id = input("Enter User ID: ")
    user_name = input("Enter User Name: ")
    print("Press 'r' to register your face. Press 'q' to exit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        
        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, "Press 'r' to register", 
                          (left + 6, top - 6),
                          cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow('Register User', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r') and face_locations:
            try:
                db = connect_to_db()
                if db:
                    cursor = db.cursor()
                    face_encoding_bytes = np.array(face_encodings[0]).tobytes()
                    
                    cursor.execute("""
                        INSERT INTO checkins (user_id, user_name, face_encoding) 
                        VALUES (%s, %s, %s)
                    """, (user_id, user_name, face_encoding_bytes))
                    
                    db.commit()
                    print(f"User {user_name} registered successfully!")
                    db.close()
                    break
            except Error as e:
                print(f"Database error: {e}")
                break
        elif key == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    register_user()