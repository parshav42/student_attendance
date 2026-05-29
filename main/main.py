

import cv2
import os
import csv
import time
import datetime
import numpy as np
import pandas as pd
from PIL import Image
import gui as gu




folders = [
    "StudentDetails",
    "TrainingImage",
    "Attendance",
    "ImagesUnknown"
]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)




student_file = "StudentDetails/StudentDetails.csv"
trainer_file = "trainer.yml"
haar_file = "haarcascade_frontalface_default.xml"



if not os.path.exists(student_file):

    with open(student_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Id", "Name"])




def insert_user():

    Id = gu.ln.get()
    name = gu.fn.get()

    if not Id.isnumeric():
        gu.v.set("ID must be numeric")
        return

    if not name.replace(" ", "").isalpha():
        gu.v.set("Name must contain only letters")
        return

    df = pd.read_csv(student_file)

    if df['Id'].astype(str).str.contains(str(Id)).any():
        gu.v.set("User already exists")
        return

    cam = cv2.VideoCapture(0)

    detector = cv2.CascadeClassifier(haar_file)

    sampleNum = 0

    while True:

        ret, img = cam.read()

        if not ret:
            gu.v.set("Camera not working")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            sampleNum += 1

            img_path = f"TrainingImage/{name}.{Id}.{sampleNum}.jpg"

            cv2.imwrite(img_path, gray[y:y+h, x:x+w])

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            cv2.putText(
                img,
                f"Samples: {sampleNum}",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        cv2.imshow("Capture Images", img)

        if cv2.waitKey(1) == ord('q'):
            break

        elif sampleNum >= 60:
            break

    cam.release()
    cv2.destroyAllWindows()

    with open(student_file, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([Id, name])

    gu.v.set(f"Images Saved for {name}")




def getImagesAndLabels(path):

    imagePaths = [
        os.path.join(path, f)
        for f in os.listdir(path)
    ]

    faceSamples = []
    ids = []

    for imagePath in imagePaths:

        pilImage = Image.open(imagePath).convert('L')

        imageNp = np.array(pilImage, 'uint8')

        Id = int(os.path.split(imagePath)[-1].split(".")[1])

        faceSamples.append(imageNp)

        ids.append(Id)

    return faceSamples, ids


def train_images():

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces, ids = getImagesAndLabels("TrainingImage")

    recognizer.train(faces, np.array(ids))

    recognizer.save(trainer_file)

    gu.v.set("Training Complete")



def track_user():

    if not os.path.exists(trainer_file):
        gu.v.set("Train images first")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read(trainer_file)

    faceCascade = cv2.CascadeClassifier(haar_file)

    df = pd.read_csv(student_file)

    cam = cv2.VideoCapture(0)

    font = cv2.FONT_HERSHEY_SIMPLEX

    col_names = ['Id', 'Name', 'Date', 'Time']

    attendance = pd.DataFrame(columns=col_names)

    while True:

        ret, img = cam.read()

        if not ret:
            gu.v.set("Camera not working")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            if conf < 60:

                user_name = df.loc[df['Id'] == Id, 'Name'].values

                if len(user_name) > 0:
                    name = user_name[0]
                else:
                    name = "Unknown"

                ts = time.time()

                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                attendance.loc[len(attendance)] = [
                    Id,
                    name,
                    date,
                    timeStamp
                ]

                display_text = f"{Id} - {name}"

                cv2.putText(
                    img,
                    display_text,
                    (x, y-10),
                    font,
                    0.8,
                    (0, 255, 0),
                    2
                )

            else:

                noOfFile = len(os.listdir("ImagesUnknown")) + 1

                cv2.imwrite(
                    f"ImagesUnknown/Image{noOfFile}.jpg",
                    img[y:y+h, x:x+w]
                )

                cv2.putText(
                    img,
                    "Unknown",
                    (x, y-10),
                    font,
                    0.8,
                    (0, 0, 255),
                    2
                )

        cv2.imshow("Track User", img)

        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    attendance = attendance.drop_duplicates(subset=['Id'])

    fileName = f"Attendance/Attendance_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    attendance.to_csv(fileName, index=False)

    gu.v.set("Attendance Saved")



def del_user():

    delete_id = gu.dn.get()

    if not delete_id.isnumeric():
        gu.v.set("Enter valid ID")
        return

    df = pd.read_csv(student_file)

    df = df[df['Id'].astype(str) != delete_id]

    df.to_csv(student_file, index=False)

    gu.v.set("User Deleted")


gu.button_submit.config(command=insert_user)

gu.button_train.config(command=train_images)

gu.button_track.config(command=track_user)

gu.button_delete.config(command=del_user)

gu.button_exit.config(command=gu.windows.destroy)

gu.windows.mainloop()
