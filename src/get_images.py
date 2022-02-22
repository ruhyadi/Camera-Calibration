from genericpath import exists
import numpy as np
import cv2
import time
import sys
import os

# Set your camera
cap = cv2.VideoCapture(0)

# Set these for high resolution
# cap.set(3, 1280)  # width
# cap.set(4, 480)  # height

i = 0

try:
    os.makedirs(sys.argv[1])
except:
    print('Directory already exist.')

def main():
    global i
    if len(sys.argv) < 4:
        print("Usage: ./program_name directory_to_save start_index prefix")
        sys.exit(1)

    i = int(sys.argv[2])
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite(sys.argv[1] + "/" + sys.argv[3] + str(i) + ".png", frame)
            i += 1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
