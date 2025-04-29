#git push from raspberry pi
#Control Variables for 3c_threaded_Mod4
import os

detect = 1 # Set to 1 for Lane detection

Testing = True# Set to True --> if want to see what the car is seeing
Profiling = False # Set to True --> If you want to profile code

debugging = True # Set to True --> If you want to debug code
clr_segmentation_tuning = True # Set to True --> If you want to tune color segmentation parameters

Detect_N_Draw = False

vid_path = os.path.abspath("Detection/Lanes/Inputs/signs_forward.mp4")
#vid_path = os.path.abspath("Detection/Lanes/Inputs/in_16_2.avi")
loopCount=0


Resized_width = 320#320#240#640#320 # Control Parameter
Resized_height = 240#240#180#480#240


if debugging:
    waitTime = 50
else:
    waitTime = 1
