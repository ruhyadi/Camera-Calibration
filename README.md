# Monocular Camera Calibration

## Get Image form Webcam
```
python get_images.py ./directory_to_save start_index prefix

python get_images.py ./data 0 images_webcam
```

## Calibrate Camera
```
python mono_calibration.py \
    --image_dir ./demo \
    --image_format jpeg \
    --prefix M30_ \
    --square_size 0.025 \
    --width 9 \
    --height 6 \
    --save_file M30_calibration.yml
```