import cv2
import numpy
import dlib

# Huge shoutout to Pysource for helping get started with facial recognition, their tutorials are fantastic!
# https://www.youtube.com/@pysource-com

# Other referenced documentation:
# https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html
# https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1
# https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html
# https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
# https://docs.opencv.org/3.4/d2/d42/tutorial_face_landmark_detection_in_an_image.html


# Returns a tuple with the midpoint values of the eye landmarks, then converts to int to get the exact pixel as you cannot have non-whole number pixels
def getMidpoint(p1, p2):
    xMidpoint = int((p1.x + p2.x) / 2)
    yMidpoint = int((p1.y + p2.y) / 2)
    midpointTuple = (xMidpoint, yMidpoint)
    return midpointTuple


detector = dlib.get_frontal_face_detector() # This is dlib's built in face detection software
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

capture = cv2.VideoCapture(0) # This will pipe in video from the webcam in index 0 on your computer
while True:
    try:
        ret, frame = capture.read()
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale

        faces = detector(grayFrame) # This will detect all faces in a frame and create an array of faces

        for face in faces: # This loop will draw over my face in a live feed
            x, y = face.left(), face.top()
            x1, y1 = face.right(), face.bottom()
            # cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2) # This will draw  a box around the detected face

            landmarks = predictor(grayFrame, face)# Get facial landmarks
            # The below code will draw a circle on the landmark spot 36
            # x = landmarks.part(43).x
            # y = landmarks.part(43).y
            # cv2.circle(frame, (x, y), 3, (0, 0, 255), 2)

            # The below code will draw a horizontal line across the left eye
            leftPointLeftEye = (landmarks.part(36).x, landmarks.part(36).y)
            rightPointLeftEye = (landmarks.part(39).x, landmarks.part(39).y)
            centerPointTopLeftEye = getMidpoint(landmarks.part(37), landmarks.part(38))
            centerPointBottomLeftEye = getMidpoint(landmarks.part(41), landmarks.part(40))

            # The below code will draw a horizontal line across the right eye
            leftPointRightEye = (landmarks.part(42).x, landmarks.part(42).y)
            rightPointRightEye = (landmarks.part(45).x, landmarks.part(45).y)
            centerPointTopRightEye = getMidpoint(landmarks.part(43), landmarks.part(44))
            centerPointBottomRightEye = getMidpoint(landmarks.part(47), landmarks.part(46))

            # Draw the horizontal lines:
            cv2.line(frame, leftPointLeftEye, rightPointLeftEye, (0, 255, 0), 2) # Left eye
            cv2.line(frame, leftPointRightEye, rightPointRightEye, (0, 255, 0), 2) # Right eye

            # Draw the vertical lines
            cv2.line(frame, centerPointTopLeftEye, centerPointBottomLeftEye, (0, 255, 0), 2)  # Left eye
            cv2.line(frame, centerPointTopRightEye, centerPointBottomRightEye, (0, 255, 0), 2)  # Right eye





        cv2.imshow("Eye In Frame w color", frame)
        key = cv2.waitKey(30)
    except Exception as e:
        if ('NoneType' in str(e)) and (frame is None):
            print('The video has ended')
            break
        else:
            print('An exception has occurred. Exception: ' + str(e))
            break
    if key == 27: # This means you have pressed s for stop on the keyboard
        break

capture.release()
cv2.destroyAllWindows()
