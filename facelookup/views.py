from django.shortcuts import render, HttpResponse, redirect
from django.http import StreamingHttpResponse
from .forms import ImageVideoForm
import numpy as np
import cv2
import os
import glob
import face_recognition
import datetime
from django.template import loader

# Create your views here.

video_time = datetime.timedelta(seconds=0)

def generate_frames():
    files = glob.glob("D:\\projects\\faceDetective\\media\\videos\\*")
    newestvid = max(files, key=os.path.getctime)

    files = glob.glob("D:\\projects\\faceDetective\\media\\images\\*")
    newestimg = max(files, key=os.path.getctime)

    video_capture = cv2.VideoCapture(newestvid)

    fps = video_capture.get(cv2.CAP_PROP_FPS)

    image = face_recognition.load_image_file(newestimg)
    face_encoding = face_recognition.face_encodings(image)[0]

    known_face_encodings = [face_encoding]

    frame_count = 0
    process_every_n_frames = 2  # Process every 2nd frame

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        frame_count += 1

        if frame_count % process_every_n_frames == 0:
            frame_resized = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # Resize for better performance
            face_locations = face_recognition.face_locations(frame_resized)
            face_encodings = face_recognition.face_encodings(frame_resized, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    cv2.rectangle(frame, (left * 2, top * 2), (right * 2, bottom * 2), (0, 0, 225), 2)
                    cv2.rectangle(frame, (left * 2, bottom * 2), (right * 2, bottom * 2), (0, 0, 225), cv2.FILLED)
                    seconds = round(frame_count / fps)
                    global video_time
                    video_time = datetime.timedelta(seconds=seconds)
                    cv2.imwrite(r'D:\projects\faceDetective\media\screenshots\found.png', frame)

        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video_capture.release()
    cv2.destroyAllWindows()


def index(request):
    if request.method == 'POST':
        form = ImageVideoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ImageVideoForm()

    return render(request, 'index.html', {'form': form})

def success_view(request):
    context = {
        'video_time': video_time,
    }
    template = loader.get_template('success.html')
    return HttpResponse(template.render(context, request))

def video_feed(request):
    response = StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
    response['Cache-Control'] = 'no-cache'
    return response
