from matplotlib.pyplot import text
from flask import Flask,render_template,Response,jsonify, request
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import cv2
import face_recognition
import numpy as np
import os
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
app=Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
CORS(app)
texts=0
Riya_image = face_recognition.load_image_file("Riya/Riya.jpg")
Riya_face_encoding = face_recognition.face_encodings(Riya_image)[0]
dhoni_image = face_recognition.load_image_file("dhoni/dhoni.jpg")
dhoni_face_encoding = face_recognition.face_encodings(dhoni_image)[0]
known_face_encodings = [
    Riya_face_encoding,
    dhoni_face_encoding
]
known_face_names = [
    "Riya",
    "dhoni"
]
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def gen_frames():
        name = "Unknown"  
        frame = cv2.imread("FILES/blob.png")   
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        if len(face_locations)!=0:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)
                

                # Display the results
            if face_locations!=0:
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4

                        # Draw a box around the face
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                        # Draw a label with a name below the face
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                        namess = "result.png"
                        cv2.imwrite(namess, frame)
            return name
        else:
            namess = "result.png"
            cv2.imwrite(namess, frame)
            return name

@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(file):
    return file.mimetype.split('/')[1] in ALLOWED_EXTENSIONS

@app.route('/result', methods=['GET', 'POST'])
def result():
    f = request.files['image']
    app.config['UPLOAD_FOLDER'] = 'FILES/'
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)) +'.png')
    return {"success": True}
@app.context_processor
def text1():
    
    if texts=="Unknown":
       return {'answer':"Please click a pic again your attendence has not been marked"}
    else:
       return {'answer':" Thank you {nam}  your attendence has been  marked..,".format(nam=texts)}
@app.route("/final1")
def main():
    global texts
    texts=gen_frames()
    return render_template('final.html')


if __name__=="__main__":
    app.run(debug=True,host='127.0.0.1')