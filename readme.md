# movie-crop
Crop movies using Python.

Open your movie, select a region with your mouse, and slick `s` (for save). It will then either save the movie or a sequence of images, depending on which parameter you choose.

Note this is a very simple tool: if you want tons of choices/features, I recommend the command-line tool `ffmpeg`. `movie-crop` is basically a front-end wrapper for that.

Dependencies: opencv 4+ and numpy.

Sample movie clip from the open-source cartoon Big Buck Bunny is provided for practicing (https://en.wikipedia.org/wiki/Big_Buck_Bunny). Note there is no sound (OpenCV does not handle audio).

## How to use
- In movie_crop.py, in the first two sections set up imports, set the parameters (see code for details).
- Run through remaining sections of the script:
    - Define functions
    - Open movie and view metadata (optional)
    - Preview movie (optional)
    - Open frame to select cropping parameters
    - Save cropped data (either image stack or as another movie)
Note OpenCV does *not* play nicely with Jupyter so run from an IDE, or break into separate files and run from the command line.

## About
This is part of an analysis pipeline developed with the Neurobehavioral Core at NIEHS:
https://www.niehs.nih.gov/research/atniehs/facilities/neurobehavioral/index.cfm

## Notes
- The standard command-line tool for movie editing is ffmpeg, and opencv typically uses it in the back end. To check in your case you can use `print(cv2.getBuildInformation())` and look for `Video I/O`.
- When making this I did a bunch of experiments saving 500 frames to movies to see which codecs went best with different file types (focusing on `mp4` and `avi` because they are the most common). Results, and other general notes, are in `supplemental.md`.

## To do
- Add a rescale option.
- Refactor code
- Clean this up.
- Add batch processing for all movies in folder.
- Option to read/save greyscale (imread(image_path, cv2.IMREAD_GRAYSCALE))
- Clicking X should work because this is 2020. But opencv is weird:
https://stackoverflow.com/questions/35003476/opencv-python-how-to-detect-if-a-window-is-closed


## To think about doing
- Put functions in a separate module?
- Have qt file open dialog
- Make into larger scale GUI application rather than program.
