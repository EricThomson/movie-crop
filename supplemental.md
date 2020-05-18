# Supplementary information with movie-crop
Stuff that didn't belong in the main readme.md but that I couldn't bear throwing away.

## Results of experimenting with differnet codecs and file types    

    codec      format   works?  size (MB)  codec decoded as
    MJPG:
                avi       y     3.9MB       MJPG
                mp4       y     3.9MB       mp4v
    Both look the same and about as good as original. Maybe mp4 a little better?

    FFV1 -- lossless compression
                avi      y      12.3       FFV1
                mp4      y      26.1       avc1
    Both look really good, basically like the original.

    H264 (X264 yielded no results in either)
                avi      n       n/a       n/a
                mp4      y       26.1      avc1
    Looks decent, but worse thatn FFV1 and the original.

    DIVX
                avi      y        0.7       DIVX
                mp4      y        0.7       mp4v
    Really good compression, really good quality: close to original. This does
    seem to be becoming the market leader for commercial streaming services.

When I tried to specify AVC1 (or avc1) as the codec for saving it didn't work for either file.

### Notes
avc1: advanced video coding is a type of H264  (maybe for apple?)
  avc1 has no start codes, while H264 does have them:
    https://docs.microsoft.com/en-us/windows/win32/directshow/h-264-video-types

mp4v: mpeg-4 video (motion picture experts group)
    mp4 also stands for mpeg-4, so basically
mjpg: motion jpeg

So basically it looks like many of these codecs are not consistent with mp4, so it just defaults to mp4v or avc1, while avi (audio video interleave) supports all of these different codecs.





## Informative stuff
- Good discussion of codecs and file formats
https://blog.filestack.com/thoughts-and-knowledge/complete-list-audio-video-file-formats/

- All four-character codecs:
 http://www.fourcc.org/codecs.php

- Useful resources for OpenCv video:
  - https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
  - https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
  - https://stackoverflow.com/questions/44947505/how-to-make-a-movie-out-of-images-in-python
  - Enumeration of capture properties:
https://docs.opencv.org/4.3.0/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
