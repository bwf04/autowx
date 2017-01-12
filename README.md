autowx
==============================
This is a rewrite of rtlsdr-automated-wxsat-capture.

Automate Recording of Low Earth Orbit NOAA Weather Satellites
License:  GPLv2 or any later version

assumptions: Linux-based computer, rtl-sdr usb dongle, stationary antenna, experienced python user

goal:  record wav files for later processing, postprocess wav file, generate image, send images using SCP

prerequistes:  working rtl-sdr, nsat/pypredict libraries, basic python libraries (subprocess, os, re, sys, time, datetime), sox, setup noaa.py/pypredict.py 

NO WARRANTY:  ALL USE IS AT THE RISK OF THE USER.  These are scripts I use for hobbyist purposes.  There may
be pre-requisites or system configuration differences which you will need to resolve in order to make use of these scripts in your project.  To do so requires patience and and, quite often, previous experience programming python 
and/or maintaining Linux-based rtl-sdr software.

This program also uses software which has no clear licensing information (wx).

##FILES

###LICENSE 
General Public License version 2.0, or any later version

###BASIC usage info
Prerequisites:

nsat/pypredict package:

git clone https://github.com/nsat/pypredict.git
cd pypredict
sudo apt-get install python-dev
sudo python setup.py install

As for wxtoimg I strongly recomment grabbing .tar.gz package and unpacking it to your /usr/local/ dir. Packages are provided on wxtoimg website.

Installing autowx:
git pull https://github.com/cyber-atomus/autowx.git


###noaa.py
This is the main python script.  It will calculate the time of the next pass for recording.  It expects to call rtl_fm to do the recording and sox to convert the file to .wav. It can create spectrogram of the pass using sox (not the RTL_POWER!).
Station options are set in the script.

####A few words about the options.

* satellites - this is a list of satellites you want to capture, this needs to be the same name as in TLE file.
* freqs - frequencies of centre of the APT signal.
* dongleGain - set this to the desired gain of the dongle, leave "0" if you want AGC.
* dongleShift - set this to the dongle PPM shift, can be negative.
* dongleIndex - set this to the index of your dongle, of you have only one - leave it unchanged.
* sample - "sample rate", option "-s" for rtl_fm - this is the width of the recorded signal. Please keep in mind that APT is 34kHz but you should include few kHz for doppler shift. This will change when the doppler tool is used.
* wavrate - sample rate of the WAV file used to generate JPEGs. Should be 11025.

####Station options (QTH)
* stationLat - Station latitude - postivie for North, negative for South
* stationLon - Station longtitude - positive for West, negative for East
* stationAlt - Station altitude
* tleDir - Directory where to look for TLE files, default /tmp (as in update-keps.sh)
* tleFile - TLE filename (as in update-keps.sh)
* minElev - Minimal elevation for prediction and record
* removeRaws - should we remove RAW wave files (before transcode)

####Directories: directories used for misc. files

* recdir - this is a directory containing RAW and WAV files.
* specdir - this is a directory holding spectrogram files created from the pass (PNG).
* imgdir - where to put output JPG images.
* mapDir - directory for autogenerated maps (these are generated using wxmap using values from predict.qth).

####WXtoIMG options
* wxAddOverlay - Should the script generate images with map overlay?
* wxEnhCreate - Create NOAA enhancements? Without this setting only raw wxtoimg decode would be created
* wxEnhList - List of NOAA enhancements script should create, look at wxtoimg documentation which enhancements are supported
* wxQuietOutput - Script won't create any output
* wxDecodeAll - the same as -A option in wxtoimg - decode everything, including noise
* wxJPEGQuality - quality of JPEG files
* wxAddTextOverlay - if the script should add custom overlay text
* wxOverlayText - Custom text
* wxOverlayOffsetX - offset map on image, negative moves map left, positive moves map right
* wxOverlayOffsetY - offset map on image, negative moves map up, positive moves map right

#####Other options
* createSpectro - creates sox spectrogram, useful for debugging 
* SCP_USER - user name for SCP-ing images and logs
* SCP_HOST - hostname for SCP-ing images
* SCP_DIR - remote directory to copy images/logs
* LOG_SCP - if the script should copy logs to remote server
* IMG_SCP - if the script should copy images to remote server
* loggingEnable - of you need noaa.py logs saved, set this to "yes"
* logFileName - log file name, including directory
* scriptPID - where to put script PID file 
* statusFile - status file name, for simple remote status (few TODOS)
* sfpgLink - if you use SFPG script it creates symlink for latest image previev, normally set it to something other than 'y', 'yes' or '1'


###pypredict.py
This is a short python module for extracting the AOS/LOS times
of the next pass for a specified satellite.  It uses nsat/pypredict for satellite prediction. Few settings:
* opoznienie - recording delay in seconds to prevent recording low elevation noise
* skrocenie - short the recording by XX seconds to prevent recording low elevation noise

###tletest.py
Small script for dumping nearest passes, few settings:
* qth() - as in pypredict QTH, example inside qth(LAT,LON,ALT)
* minEl - minimum elevation

###update-keps.sh
This is a short shell script to update the keps, which are orbital
parameters needed by the predict program.  It is mostly copied from the PREDICT man
page. 
