# -*- coding: utf-8 -*-
"""
movie_crop.py

Simple script to crop a movie. Part of movie-crop repo. See movie-crop/readme.md 

Uses a lot of previous code I wrote for im-crop: 
    https://github.com/EricThomson/im-crop/blob/master/image_cropper.py
"""

import os
from pathlib import Path
import numpy as np
import cv2


#%%  SET PARAMETERS
"""
PARAMETERS USED IN REST OF SCRIPT
window_params: 
    are for display of the original movie you want to crop.
movie_path: 
    where is the movie you want to open and crop?
output_path: 
    folder where you want to save the cropped data
save_filename:
    name of the movie you want to create. new movie will be this + filetype.
save_filetype: 
    type of file (avi/mp4 for movies is good), set to png for image stack
codec: 
    four-digit codec for movie (FFVI is lossless, DIVX makes them very small)
    Ignored for image stack (i.e., when save_filetype is png)
frame_to_crop:
    for cropping, which frame number to use? Some movies start with a black
    fade-in or objects absent that make it hard to pick a good region.
num_to_preview: 
    how many frames do you want to preview? Set to 0 if none.
num_to_save: 
    how many frames do you want to save? (maybe just default to all)
save_fps: 
    control frames per second of new cropped movie
line_width: 
    Width of rectangle to draw with mouse
line_color: 
    (b, g, r) color of rectangle -- bgr because opencv is weird
"""
window_params = {'width': 1280, 'height': 720, 'x': 2400, 'y': 100}
movie_path = Path(r'./big_bunny.mp4')
output_path = Path(r'./saved')
save_filename = 'test' # filename will be save_filename + save_filetype (or stem + ### + filetype)
save_filetype = 'avi'  # avi and mp4 are good.png means use image stack.
codec = 'FFV1'     #'FFV1' is lossless. 'DIVX' is super efficient. Ignored for png
frame_to_crop = 100
num_to_preview = 300  #set to 0 if you don't want preview
num_to_save = 550
save_fps = 15
line_width = 4            # line for rectangle you are drawing
line_color = (0, 0, 255)  #remember cv2 is bgr -- this is red
# Create output directory if needed
if os.path.isdir(output_path):
    pass
else:
    os.mkdir(output_path)
    
#%% DEFINE FUNCTIONS
def decode_codec(x):
    """
    Convert float returned from OpenCV to four character codec.
    
    Adapted from https://stackoverflow.com/a/61681888/1886357
    """
    h = int(x)
    codec_str = chr(h&0xff) + chr((h>>8)&0xff) + chr((h>>16)&0xff) + chr((h>>24)&0xff) 
    return codec_str

def print_movie_info(length, height, width, fps, codec_code):
    """ 
    Print out metadata about movie
    """
    print(f"Movie has {length} frames that are {width}x{height} (wxh).")
    print(f"It is showing at {fps} fps.")
    print(f"It is compressed with the {codec_code} codec.")

def mouse_callback(event, x, y, flags, param):
    """
    Used for drawing box on image_to_show with mouse press.
    
    Adapted from OpenCv 3 and Computer Vision with Python Cookbook.
    """
    global image, image_to_show, s_x, s_y, e_x, e_y, mouse_pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_pressed = True
        s_x, s_y = x, y
        image_to_show = np.copy(image)
    elif event == cv2.EVENT_MOUSEMOVE:
        if mouse_pressed:
            image_to_show = np.copy(image)
            cv2.rectangle(image_to_show, 
                          (s_x, s_y),
                          (x, y), 
                          line_color, 
                          line_width)
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_pressed = False
        e_x, e_y = x, y
        box_width = abs(e_x - s_x)
        box_height = abs(e_y - s_y)
        print(s_x, s_y, e_x, e_y)
        print(f"    Height/Width: {box_height}/{box_width}")


#%% OPEN MOVIE AND VIEW METADATA (optional)
movie_name = movie_path.stem
movie = cv2.VideoCapture(str(movie_path))
if (movie.isOpened() == False):
    print("Sorry movie did not open")
else:
    movie_length = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_height = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width =  int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(movie.get(cv2.CAP_PROP_FPS))
    ms_per_frame = 1000//fps
    codec_code =  movie.get(cv2.CAP_PROP_FOURCC)
    print(f"Movie opened successfully.")
   
codec_chars = decode_codec(codec_code)
print_movie_info(movie_length, frame_height, frame_width, fps, codec_chars)
if num_to_preview > movie_length:
    print(f"Reducing preview to {movie_length}.")
    num_to_preview = movie_length
    

#%% PREVIEW MOVIE (optional) 
# hit escape once to stop, and again to close window
print(f"\nPreviewing {num_to_preview} frames.")
preview_window_name = 'PREVIEW (esc to close)'
if num_to_preview > 0:
    movie = cv2.VideoCapture(str(movie_path))
    frame_num = 0
    cv2.namedWindow(preview_window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(preview_window_name, 
                     window_params['width'], 
                     window_params['height'])  #width, height
    cv2.moveWindow(preview_window_name, 
                   window_params['x'], 
                   window_params['y'])
    while(frame_num <= num_to_preview and movie.isOpened()):
        ret, frame = movie.read()
        if ret:
            cv2.imshow(preview_window_name, frame)
            k = cv2.waitKey(ms_per_frame)
            if k == 27:
                break
            frame_num += 1
        else:
            print(f"{frame_num} did not read correctly. Exiting.")
            break
k = cv2.waitKey()
if k == 27:
    movie.release()
    cv2.destroyAllWindows()
print("Movie preview done")
        

#%%  GET CROPPING PARAMETERS FROM ONE FRAME  
cropping_window_name = 'CROPPING (s to save)'
print("\nOpening cropping window:\nUse mouse to select cropping window.")
print("Click s to accept crop window, esc to close.")
mouse_pressed = False
s_x = s_y = e_x = e_y = -1
crop_params = {'xs': 0, 'ys': 0, 'xe': frame_width, 'ye': frame_height}
cv2.namedWindow(cropping_window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(cropping_window_name, window_params['width'], window_params['height'])  #width, height
cv2.moveWindow(cropping_window_name, window_params['x'], window_params['y'])
cv2.setMouseCallback(cropping_window_name, mouse_callback)

movie = cv2.VideoCapture(str(movie_path))
movie.set(cv2.CAP_PROP_POS_FRAMES, frame_to_crop-1)
ret, image = movie.read()
image_to_show = image.copy() # np.copy(image)
while True:
    cv2.imshow(cropping_window_name, image_to_show)
    k = cv2.waitKey(1)
    # s is save
    if k == ord('s'):
        print('Crop prameters set')
        if s_y > e_y:
            s_y, e_y = e_y, s_y
        if s_x > e_x:
            s_x, e_x = e_x, s_x
        crop_width = e_x - s_x
        crop_height = e_y - s_y
        if crop_height > 2 and crop_width > 2:
            crop_params['xs'] = s_x
            crop_params['ys'] = s_y
            crop_params['xe'] = e_x
            crop_params['ye'] = e_y
        else:
            print("Minimum width/height of cropped region is 2. Try again.")
    elif k == 27:
        break
k = cv2.waitKey()
if k == 27:
    print(crop_params)
    movie.release()
    cv2.destroyAllWindows()
print("Done setting crop parameters")

"""
movie_path = Path(r'./test.mp4')
output_path = Path(r'./saved')
save_filename = 'test' # filename will be save_filename + save_filetype (or stem + ### + filetype)
save_filetype = 'avi'  # avi and mp4 are good.png means use image stack.
"""

#%% SAVE CROPPED DATA WITH NEW PARAMETERS
# Save num_to_save frames to image stack if png specified, 
# movie if avi/mp4 and codec specified
xs = crop_params['xs']
ys = crop_params['ys']
xe = crop_params['xe']
ye = crop_params['ye']

movie = cv2.VideoCapture(str(movie_path))
if save_filetype == 'png': # Image stack
    image_save_path = output_path / r'images'

    if num_to_save > 0:
        frame_num = 0       
        while(frame_num <= num_to_save and movie.isOpened()):
            print(f"Saving cropped frame number {frame_num} out of {num_to_save}")
            ret, frame = movie.read()
            if ret:
                if frame.ndim == 2:
                    cropped_frame = frame[ys: ye, xs: xe]
                else:
                    cropped_frame = frame[ys: ye, xs: xe, :]
                image_name = f"{save_filename}_{frame_num:03d}" + r".png"
                image_path = image_save_path / image_name
                cv2.imwrite(str(image_path), cropped_frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])
                frame_num += 1
            else:
                print(f"{frame_num} did not read correctly. Exiting.")
                break
        movie.release()
    else:
        print("You set num_to_save as 0 or fewer.")
    print("Saving cropped image stack done.")

else: # Movie
    width = xe - xs
    height = ye - ys
    frame_size = (width, height)    
    save_cc_code = cv2.VideoWriter_fourcc(codec[0], 
                                          codec[1], 
                                          codec[2], 
                                          codec[3])
    movie_name = save_filename + r'.' + save_filetype
    save_path = output_path / movie_name
    movie_out = cv2.VideoWriter(str(save_path), save_cc_code, save_fps, frame_size )
    if num_to_save > 0:
        frame_num = 0       
        while(frame_num <= num_to_save and movie.isOpened()):
            if frame_num % 50 == 0:
                print(f"Writing cropped frame number {frame_num} out of {num_to_save}")
            ret, frame = movie.read()
            if ret:
                if frame.ndim == 2:
                    cropped_frame = frame[ys: ye, xs: xe]
                else:
                    cropped_frame = frame[ys: ye, xs: xe, :]               
                movie_out.write(cropped_frame)
                frame_num += 1
            else:
                print(f"{frame_num} did not read correctly. Exiting.")
                break
        movie.release()
        movie_out.release()
    else:
        print("You set num_to_save as 0 or fewer. Exiting.")
    print("Saving cropped movie done")