import cv2
import numpy
import dlib
from math import hypot
import datetime
from KeyboardAndMouseController import mouseController, keyboardController

# Author: Lev Vinokur

# Huge shoutout to Pysource for helping get started with facial recognition, their tutorials are fantastic!
# https://www.youtube.com/@pysource-com

# Other referenced documentation:
# https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html
# https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1
# https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html
# https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
# https://docs.opencv.org/3.4/d2/d42/tutorial_face_landmark_detection_in_an_image.html
# https://www.geeksforgeeks.org/python-math-function-hypot/


# Returns a tuple with the midpoint values of the eye landmarks, then converts to int to get the exact pixel as you cannot have non-whole number pixels
def getMidpoint(p1, p2):
    xMidpoint = int((p1.x + p2.x) / 2)
    yMidpoint = int((p1.y + p2.y) / 2)
    midpointTuple = (xMidpoint, yMidpoint)
    return midpointTuple


# Declare global variables:
detector = dlib.get_frontal_face_detector() # This is dlib's built in face detection software
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
capture = cv2.VideoCapture(0) # This will pipe in video from the webcam in index 0 on your computer
font = cv2.FONT_HERSHEY_PLAIN
mouse = mouseController()
keyboard = keyboardController()

# Declare counters:
leftWinkCounter = 0
rightWinkCounter = 0
blinkCounter = 0

while True:
    try:
        ret, frame = capture.read()
        frame = cv2.flip(frame, 1) # Convert the frame to a mirror image of the video feed
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

            # Get all landmark points for the left eye
            leftEyeLeftPoint = (landmarks.part(36).x, landmarks.part(36).y)
            leftEyeRightPoint = (landmarks.part(39).x, landmarks.part(39).y)
            leftEyeCenterPointTop = getMidpoint(landmarks.part(37), landmarks.part(38))
            leftEyeCenterPointBottom = getMidpoint(landmarks.part(41), landmarks.part(40))

            # Get all landmark points for the right eye
            rightEyeLeftPoint = (landmarks.part(42).x, landmarks.part(42).y)
            rightEyeRightPoint = (landmarks.part(45).x, landmarks.part(45).y)
            rightEyeCenterPointTop = getMidpoint(landmarks.part(43), landmarks.part(44))
            rightEyeCenterPointBottom = getMidpoint(landmarks.part(47), landmarks.part(46))

            # Draw horizontal lines across both eyes:
            leftEyeHorizontalLine = cv2.line(frame, leftEyeLeftPoint, leftEyeRightPoint, (0, 255, 0), 2) # Left eye
            rightEyeHorizontalLine = cv2.line(frame, rightEyeLeftPoint, rightEyeRightPoint, (0, 255, 0), 2) # Right eye

            # Draw vertical lines across both eyes
            leftEyeVerticalLine = cv2.line(frame, leftEyeCenterPointTop, leftEyeCenterPointBottom, (0, 255, 0), 2)  # Left eye
            rightEyeVerticalLine = cv2.line(frame, rightEyeCenterPointTop, rightEyeCenterPointBottom, (0, 255, 0), 2)  # Right eye

            # Determine if user has blinked by calculating length of vertical lines in eyes and by checking if the users retina has disappeared for a certain amount of frames
            leftEyeVerticalLineLength = hypot((leftEyeCenterPointTop[0] - leftEyeCenterPointBottom[0]), (leftEyeCenterPointTop[1] - leftEyeCenterPointBottom[1]))
            leftEyeHorizontalLineLength = hypot((leftEyeLeftPoint[0] - leftEyeRightPoint[0]), (leftEyeLeftPoint[1] - leftEyeRightPoint[1]))

            rightEyeHorizontalLineLength = hypot((rightEyeLeftPoint[0] - rightEyeRightPoint[0]), (rightEyeLeftPoint[1] - rightEyeRightPoint[1]))
            rightEyeVerticalLineLength = hypot((rightEyeCenterPointTop[0] - rightEyeCenterPointBottom[0]), (rightEyeCenterPointTop[1] - rightEyeCenterPointBottom[1]))

            # Number is bigger when eye is closed than when it is not
            # print(str(datetime.datetime.now()) + " Left eye: " + str(leftEyeHorizontalLineLength/leftEyeVerticalLineLength))
            # print(str(datetime.datetime.now()) + " Right eye: " + str(rightEyeHorizontalLineLength/rightEyeVerticalLineLength))

            # Get eye ratios
            leftEyeRatio = (leftEyeHorizontalLineLength/leftEyeVerticalLineLength)
            rightEyeRatio = (rightEyeHorizontalLineLength/rightEyeVerticalLineLength)

            # NOTE: We have 12 frames per second

            if (rightEyeRatio > 4.9) and (leftEyeRatio > 4.9):
                blinkCounter += 1
                cv2.putText(frame, "BLINK", (50, 150), font, 7, (255, 0, 0))
                if blinkCounter == 2:  # This means that both eyes have been closed for 2 frames
                    print("LONG BLINK")
            else:
                blinkCounter = 0

            if (leftEyeRatio > 4.9) and (rightEyeRatio < 4.9):
                leftWinkCounter += 1
                cv2.putText(frame, "LEFT WINK", (50, 150), font, 7, (255, 0, 0))
                if leftWinkCounter == 2: # This means that the left eye has been closed for 2 frames
                    mouse.mouseLeftClick()
            else:
                leftWinkCounter = 0

            if (rightEyeRatio > 4.9) and (leftEyeRatio < 4.9):
                rightWinkCounter += 1
                cv2.putText(frame, "RIGHT WINK", (50, 150), font, 7, (255, 0, 0))
                if rightWinkCounter == 2:  # This means that the right eye has been closed for 2 frames
                    mouse.mouseRightClick()
            else:
                rightWinkCounter = 0


            # TODO: Gaze detection

            leftEyeMap = numpy.array([(landmarks.part(36).x, landmarks.part(36).y), (landmarks.part(37).x, landmarks.part(37).y), (landmarks.part(38).x, landmarks.part(38).y), (landmarks.part(39).x, landmarks.part(39).y), (landmarks.part(40).x, landmarks.part(40).y), (landmarks.part(41).x, landmarks.part(41).y)], numpy.int32)

            rightEyeMap = numpy.array([(landmarks.part(42).x, landmarks.part(42).y), (landmarks.part(43).x, landmarks.part(43).y), (landmarks.part(44).x, landmarks.part(44).y), (landmarks.part(45).x, landmarks.part(45).y), (landmarks.part(46).x, landmarks.part(46).y), (landmarks.part(47).x, landmarks.part(47).y)], numpy.int32)

            # EXAMPLE CODE DEMONSTRATING THE MATH CONCEPTS NEEDED TO CALCULATE THE CENTER OF A PERSON'S EYE AT ANY GIVEN TIME:

            # https://www.geeksforgeeks.org/finding-quadrant-coordinate-respect-circle/
            # Python3 Program to find the
            # quadrant of a given coordinate
            # w.rt. the centre of a circle
            import math


            # This function returns the
            # quadrant number
            # def getQuadrant(X, Y, R, PX, PY):
            #
            #     # Coincides with center
            #     if (PX == X and PY == Y):
            #         return 0;
            #
            #     val = (math.pow((PX - X), 2) +
            #            math.pow((PY - Y), 2));
            #
            #     # Outside circle
            #     if (val > pow(R, 2)):
            #         return -1;
            #
            #     # 1st quadrant
            #     if (PX > X and PY >= Y):
            #         return 1;
            #
            #     # 2nd quadrant
            #     if (PX <= X and PY > Y):
            #         return 2;
            #
            #     # 3rd quadrant
            #     if (PX < X and PY <= Y):
            #         return 3;
            #
            #     # 4th quadrant
            #     if (PX >= X and PY < Y):
            #         return 4;
            #
            #
            # # Driver Code
            # # Coordinates of centre
            # X = 0;
            # Y = 3;
            #
            # # Radius of circle
            # R = 2;
            #
            # # Coordinates of the given po
            # PX = 1;
            # PY = 4;
            #
            # ans = getQuadrant(X, Y, R, PX, PY);
            # if (ans == -1):
            #     print("Lies Outside the circle");
            # elif (ans == 0):
            #     print("Coincides with centre");
            # else:
            #     print(ans, "Quadrant");
            #
            # # This code is contributed by mits

            # https: // stackoverflow.com / questions / 66010530 / how - to - find - point - inside - an - ellipse

            # print('leftEyeMap: ')
            # print(leftEyeMap)
            # print('rightEyeMap: ')
            # print(rightEyeMap)


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
