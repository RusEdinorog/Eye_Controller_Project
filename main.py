import cv2
import numpy

# def eyeController(name):
#     print('Useless!')


# if __name__ == '__main__':
#     eyeController('PyCharm')


# The code below is a mock-up of the eye capture portion of this project which uses a pre-recorded video to test with
capture = cv2.VideoCapture("Eye_Capture_3.mp4")
while True:
    try:
        ret, frame = capture.read()
        eyeInFrame = frame[55:500, 1000:1500]  # Cut the eye out from the rest of the frame
        rows, columns, channels = eyeInFrame.shape # This gets us the size of the images coming in by their pixels
        grayEyeInFrame = cv2.cvtColor(eyeInFrame, cv2.COLOR_BGR2GRAY)  # Convert the eye frame to grayscale
        grayEyeInFrame = cv2.GaussianBlur(grayEyeInFrame, (7, 7), 0) # Adding Gaussian blur smoothes the video feed

        _, thresh = cv2.threshold(grayEyeInFrame, 25, 255, cv2.THRESH_BINARY_INV) # This makes only the darkest portion of the video visible, which is the pupil in this case
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True) # This sorts the contours, then calculates their area using the lambda expression with the returned contourArea, then reverses the order that way the largest area contour is first in the list

        # TODO: in this for loop we can get even more creative and say that if the current contour is a certain amount smaller than some pre-defined amount for a defined period of time, then we can assume that the eye is closed
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour) # Draw center of contour
            cv2.drawContours(eyeInFrame, [contour], -1, (0, 0, 255), 3) # This function draws an array of contours, specifically in red in this case (0 blue, 0 green, 255 red) and 3 pixels thick
            cv2.rectangle(eyeInFrame, (x, y), (x + w, y + h), (255, 0, 0), 2) # This will draw a rectangle around the center point of the current contour
            cv2.line(eyeInFrame, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2) # This draws a vertical line over the center of the square
            cv2.line(eyeInFrame, (0, y + int(h / 2)), (columns, y + int(h / 2)), (0, 255, 0), 2) # This draws a horizontal line over the center of the square
            break # We can break out of the contours loop after the first as we are only trying to draw on the largest contour, which is the center of the eye

        cv2.imshow("Eye In Frame", thresh)
        cv2.imshow("Eye In Frame w color", eyeInFrame)
        key = cv2.waitKey(30)
    except Exception as e:
        if ('NoneType' in str(e)) and (frame is None):
            print('The video has ended')
            break
        else:
            print('An exception has occurred. Exception: ' + str(e))
            break
    if key == 27:
        break

cv2.destroyAllWindows()
