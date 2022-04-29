"""
Get images from webcam
"""

import cv2
import argparse

def get_images(webcam: int, output: str):
    # get webcam camera
    cap = cv2.VideoCapture(webcam)

    if not cap.isOpened():
        print('[INFO] Cannot open camera...')
        exit()

    # images ids for saving
    ids = 0

    while (True):
        ret, frame = cap.read()
        if not ret:
            print("[INFO] Can't receive frame (stream end?). Exiting ...")
            break

        cv2.imshow('Get Images', frame)
        
        if cv2.waitKey(1) == ord('s'):
            cv2.imwrite(f'output_{ids:02d}.png', frame)
            ids = ids + 1
            print(f'[INFO] Capture {ids} images')

        if cv2.waitKey(1) == ord('q'):
            print('[INFO] Streaming end...')
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Camera calibration')
    parser.add_argument('--webcam', type=int, default=0, help='Webcam number, default 0')
    parser.add_argument('--output', type=str, default='mono', help='Webcam number, default 0')

    cfg = parser.parse_args()

    get_images(cfg.webcam, cfg.output)