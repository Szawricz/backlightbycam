"""The luminosity-depended Windows screenbacklight autocontrol script"""
# coding: utf-8

import numpy
import os
from pyautogui import screenshotUtil
import subprocess
import math
from skimage import io
from skimage import color
from urllib import request

# The problem:
# Once for a timerange take the ambient luminosity value and use it for
# the LED-screen backlight setup.

# Take the username
username = subprocess.check_output(['echo', r'%username%'],
                                   encoding='utf-8', shell=True)

# check CommandCam exists and...
path = 'C:/Users/{}/Downloads/CommandCam/'.format(username.replace('\n', ''))
link = 'https://github.com/tedburke/CommandCam/blob/master/\
        CommandCam.exe?raw=true'

# ...if it is not then download
if not os.path.exists(path):
    os.makedirs(path)
    request.urlretrieve(link, '{}CommandCam.exe'.format(path))

# The waiting time before webcam frame taking
delay = 500

# Setting
# k =

# The luminance highest posible value
max_lum = 0.17637037530572403

while True:
    # Run CommandCam
    subprocess.run(['cd', path, '&&', 'CommandCam.exe', '/delay', str(delay)],
    shell=True)

    # Calculate taken file luminance nean value
    filename = os.path.join(path, 'image.bmp')
    rgb_array = io.imread(filename)
    srgb_array = color.convert_colorspace(rgb_array, 'RGB', 'RGB CIE')
    luminance_array = color.rgb2gray(srgb_array)
    lum_cam = numpy.mean(luminance_array)
    print(lum_cam)

    # # Take screenshot
    # screenshotUtil.screenshot('{}screen.png'.format(path))

    # # Calculate taken file luminance nean value
    # filename = os.path.join(path, 'screen.png')
    # rgb_array = io.imread(filename)
    # srgb_array = color.convert_colorspace(rgb_array, 'RGB', 'RGB CIE')
    # luminance_array = color.rgb2gray(srgb_array)
    # lum_scr = numpy.mean(luminance_array)

    # Calculate backlight value
    backlight = math.trunc(100*(math.sqrt(lum_cam/max_lum)))
    print(backlight)

    # Set the backlight value
    subprocess.Popen(['powershell', '(Get-WmiObject -Namespace root/WMI -Class \
    WmiMonitorBrightnessMethods).WmiSetBrightness(1, {})'.format(backlight)])
