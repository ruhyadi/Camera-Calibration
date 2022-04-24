import cv2
import numpy as np
from utils import save_coefficients, save_kitti

import argparse
import os

def calibrate_mono(
    images_dir: str, 
    columns: int, 
    rows: int, 
    square_size: int, 
    save_type: str, 
    output: str
    ):
    """
    Calibrate monocular camera
    ARGS:
        image_dir: images directory
        columns: num corners in columns of chessboard
        rows: num corners in rows of chessboard
        square_size: square size of chessboard pattern
        save_type: type of mtx file (opencv, kitti)
        output: output name
    """
    
    # get images
    imgs = os.listdir(images_dir)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
    objp = np.zeros((columns*rows, 3), np.float32)
    objp[:, :2] = np.mgrid[0:columns, 0:rows].T.reshape(-1, 2)

    objp = objp * square_size # create real world coords

    # Arrays to store object points and image points from all the images.
    OBJPOINTS = []  # 3d point in real world space
    IMGPOINTS = []  # 2d points in image plane.

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    for fname in imgs:
        # read image in grayscale
        img = cv2.imread(os.path.join(images_dir, fname), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # find chessboard pattern
        ret, corners = cv2.findChessboardCorners(
            gray, 
            patternSize=(columns, rows), 
            flags=cv2.CALIB_CB_ADAPTIVE_THRESH
            )
        
        # continue if chessboard found on images
        if ret==True:
            # store objpoints
            OBJPOINTS.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            IMGPOINTS.append(corners2)

            # draw corners on image
            img_draw = cv2.drawChessboardCorners(img, (columns, rows), corners2, ret)

        cv2.imshow('Monocular Calibration', img)
        cv2.waitKey(500)

    # store matrix
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(OBJPOINTS, IMGPOINTS, gray.shape[::-1], None, None)
    
    # save matrix in file
    if save_type=='opencv':
        save_coefficients(mtx, dist, output)
    elif save_type=='kitti':
        save_kitti(mtx, dist, output)
    else:
        return [ret, mtx, dist, rvecs, tvecs] 

if __name__ == '__main__':
    # Check the help parameters to understand arguments
    parser = argparse.ArgumentParser(description='Camera calibration')
    parser.add_argument('--images_dir', type=str, help='image directory path')
    parser.add_argument('--square_size', type=float, help='chessboard square size')
    parser.add_argument('--columns', type=int, help='chessboard width size, default is 9')
    parser.add_argument('--rows', type=int, help='chessboard height size, default is 6')
    parser.add_argument('--save_type', type=str, help='Type of save file format [yaml, kitti(txt)]')
    parser.add_argument('--output', type=str, help='Output file name with format')

    args = parser.parse_args()

    res = calibrate_mono(
        args.images_dir,
        args.columns,
        args.rows,
        args.square_size,
        args.save_type,
        args.output)