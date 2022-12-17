import cv2
import numpy

# def eyeController(name):
#     print('Useless!')


# if __name__ == '__main__':
#     eyeController('PyCharm')


# The code below is a mock-up of the eye capture portion of this project which uses a pre-recorded video to test with
capture = cv2.VideoCapture("Eye_Capture_3.mp4")
while True:
    ret, frame = capture.read()
    eyeInFrame = frame[55:500, 900:1600]  # Cut the eye out from the rest of the frame
    eyeInFrame = cv2.cvtColor(eyeInFrame, cv2.COLOR_BGR2GRAY)  # Convert the eye frame to grayscale
    _, threshold = cv2.threshold(eyeInFrame, 5, 255, cv2.THRESH_BINARY) #
    cv2.imshow("Frame", eyeInFrame)
    key = cv2.waitKey(30)

    if key == 27:
        break

cv2.destroyAllWindows()
