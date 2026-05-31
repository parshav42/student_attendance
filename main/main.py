

import cv2
import os
import csv
import time
import datetime

import numpy       as np
import pandas      as pd
import PIL.Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def p(relative_path):
    return os.path.join(BASE_DIR, relative_path)


TRAINING_IMAGE_DIR  = p("TrainingImage")
STUDENT_DETAILS_CSV = p("StudentDetails/StudentDetails.csv")
TRAINER_FILE        = p("recognizers/Trainner.yml")
ATTENDANCE_FILE     = p("Attendance/in.json")
UNKNOWN_IMG_DIR     = p("ImagesUnknown")

# ── Auto-locate haarcascade ──────────────────────────────────
_haar_local = p("haarcascade_frontalface_default.xml")
if os.path.exists(_haar_local):
    HAAR_CASCADE = _haar_local
else:
    HAAR_CASCADE = os.path.join(
        os.path.dirname(cv2.__file__),
        "data",
        "haarcascade_frontalface_default.xml"
    )

print(f"[INFO] Haarcascade : {HAAR_CASCADE}")

# ── Create required folders if they don't exist ─────────────
for folder in [TRAINING_IMAGE_DIR,
               os.path.dirname(STUDENT_DETAILS_CSV),
               os.path.dirname(TRAINER_FILE),
               os.path.dirname(ATTENDANCE_FILE),
               UNKNOWN_IMG_DIR]:
    os.makedirs(folder, exist_ok=True)

# ── Create StudentDetails.csv with header if missing ────────
if not os.path.exists(STUDENT_DETAILS_CSV):
    with open(STUDENT_DETAILS_CSV, 'w', newline='') as f:
        csv.writer(f).writerow(['Id', 'Name'])



def insert_user(fn, ln, v):
    Id   = ln.get()
    name = fn.get()

    if not (Id.isnumeric() and name.isalpha()):
        v.set("Enter valid Name (letters only) and ID (numbers only)")
        return

    df = pd.read_csv(STUDENT_DETAILS_CSV)
    if df['Id'].astype(str).str.contains(str(Id)).any():
        v.set("User with same Roll No. Already exists")
        return

    cam      = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(HAAR_CASCADE)

    if detector.empty():
        v.set("ERROR: Could not load haarcascade file!")
        return

    sampleNum = 0

    while True:
        ret, img = cam.read()
        gray     = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces    = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sampleNum += 1
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            img_path = os.path.join(TRAINING_IMAGE_DIR,
                                    f"{name.lower()}.{Id}.{sampleNum}.jpg")
            cv2.imwrite(img_path, gray[y:y+h, x:x+w])
            cv2.imshow('Capturing Face - press q to quit', img)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        if sampleNum > 60:
            break

    cam.release()
    cv2.destroyAllWindows()

    with open(STUDENT_DETAILS_CSV, 'a+', newline='') as csvFile:
        csv.writer(csvFile).writerow([Id, name])

    v.set(f"ID : {Id}  |  Name : {name}  –  Saved successfully")



def train_image(v):

    # Guard: nothing to train if folder is empty
    image_files = [f for f in os.listdir(TRAINING_IMAGE_DIR)
                   if f.lower().endswith('.jpg')]
    if not image_files:
        v.set("No images found – please register a user first")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    def load_images_and_ids(path):
        faces, ids = [], []
        for filename in os.listdir(path):
            if not filename.lower().endswith('.jpg'):
                continue
            img_path = os.path.join(path, filename)
            gray_img = PIL.Image.open(img_path).convert('L')
            img_arr  = np.array(gray_img, 'uint8')
            user_id  = int(filename.split(".")[1])
            faces.append(img_arr)
            ids.append(user_id)
        return faces, ids

    faces, ids = load_images_and_ids(TRAINING_IMAGE_DIR)
    recognizer.train(faces, np.array(ids))
    recognizer.save(TRAINER_FILE)
    v.set("Model trained and saved – you can now Track Users")



def track_user(v):

    # Guard: model must be trained first
    if not os.path.exists(TRAINER_FILE):
        v.set("No trained model found – please click Train Images first")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER_FILE)

    cam      = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(HAAR_CASCADE)
    font     = cv2.FONT_HERSHEY_SIMPLEX

    df         = pd.read_csv(STUDENT_DETAILS_CSV)
    attendance = pd.DataFrame(columns=['ID', 'Date', 'Time'])

    while True:
        ret, img = cam.read()
        gray     = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces    = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            user_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            now      = time.time()
            date_str = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d')
            time_str = datetime.datetime.fromtimestamp(now).strftime('%H:%M:%S')

            if confidence > 90:
                label = "Unknown"
                count = len(os.listdir(UNKNOWN_IMG_DIR)) + 1
                cv2.imwrite(
                    os.path.join(UNKNOWN_IMG_DIR, f"Image{count}.jpg"),
                    img[y:y+h, x:x+w]
                )
            else:
                name  = df.loc[df['Id'] == user_id]['Name'].values
                label = f"{user_id} - {name[0] if len(name) else 'N/A'}"
                attendance.loc[len(attendance)] = [user_id, date_str, time_str]

            cv2.putText(img, label, (x+w, y+h), font, 0.5,
                        (0, 255, 255), 2, cv2.LINE_AA)

        attendance.drop_duplicates(subset=['ID'], keep='first', inplace=True)
        attendance.to_json(ATTENDANCE_FILE, orient="index")

        cv2.imshow('Attendance Tracker - press q to stop', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    v.set("Attendance saved to Attendance/in.json")



def del_user(dn, v):
    del_id = dn.get()

    if not del_id.isnumeric():
        v.set("Please enter a valid numeric ID to delete")
        return

    df = pd.read_csv(STUDENT_DETAILS_CSV)

    if not df['Id'].astype(str).str.contains(del_id).any():
        v.set(f"No user found with ID : {del_id}")
        return

    df = df[df['Id'].astype(str) != del_id]
    df.to_csv(STUDENT_DETAILS_CSV, index=False)
    v.set(f"User with ID : {del_id} deleted successfully")