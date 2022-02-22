import cv2
import numpy as np
import argparse
import glob
import os
from calibration_store import load_coefficients

# read image
def undistortion(image_dir, calib, output_dir):

    if output_dir is not None:
        try:
            os.makedirs(output_dir)
        except:
            print('Directory exist')

    images = glob.glob(image_dir + '/' + '*')

    i = 0
    for fname in images:
        img = cv2.imread(fname)
        h, w = img.shape[:2]
        mtx, dist = load_coefficients(calib)

        newMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))

        newImg = cv2.undistort(img, mtx, dist, None, newMtx)
        x, y, w, h = roi
        newImg = newImg[y: y+h, x: x+w]

        # combining distortion and undistortion image
        combImg = np.hstack((img, newImg))

        cv2.imshow('Undistortion', combImg)
        cv2.waitKey(500)

        if output_dir is not None:
            cv2.imwrite(f'{output_dir}/undis{i:02d}.png', newImg)
            i = i + 1

if __name__ == '__main__':
    # Check the help parameters to understand arguments
    parser = argparse.ArgumentParser(description='Camera calibration')
    parser.add_argument('--image_dir', type=str, required=True, help='image directory path')
    parser.add_argument('--calib', type=str, required=True, help='YAML calib file')
    parser.add_argument('--output_dir', type=str, required=False, help='Output image directory path')

    args = parser.parse_args()

    print('Undistortion Image')
    undistortion(args.image_dir, args.calib, args.output_dir)