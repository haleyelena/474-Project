# 474-Project: MedRhythms Auditory Device
For the BME Design Fellows Program, my team created a breathing device that 
incorporated visual and auditory feedback in order to increase neurologic music 
therapy treatment compliance for patients suffering from Dysarthria as a result
of neurological injury (TBI and stroke) or neurodegenerative conditions 
(Parkinson's and MS) in order to improve respiratory capacity and endurance. 
These patients normally struggle to comply to their breathing exercises as the
current solutions are not entertaining, don’t have any feedback, and have no 
aspects of entrainment. This repository contains all python code used to create 
the computer side software for the device. This ReadMe serves as an instruction
manual for how to successfully use and download the software in its current state.

## Initial Software Setup Instructions
1. Pull entire main branch of this repository to your local computer and open 
in your development environment of choice. 
2. Copy 'test' folder from repository to your local Desktop. This folder contains 
the audio files necessary to use this program.
3. Correct test folder location in Calibration and Main Program scripts.
    1. Open `calibration.py` and go to line 54. Change the test folder location
    as needed to match where you have put the test folder containing the audio
       files. The current code is defaulted to `Users/haley/Desktop`, which is
       where my test folder is located on my Mac. 
   2. Open `mainprogram.py` and go to line 60. Change the test folder location
    as needed to match where you have put the test folder containing the audio
       files. The current code is defaulted to `Users/haley/Desktop`, which is
       where my test folder is located on my Mac. Repeat on lines 62 and 342. 
4. Correct serial port number in Calibration and Main Program scripts.
    1. Plug in the mechanical device to computer. Turn device on. Open arduino,
       click the "tools" drop-down, and click port in order to check the serial 
       port number that the device is connected to. 
   2. Open `calibration.py` and go to line 116. Change the serial port number to 
      match the one the device is currently connected to, as seen in the 
      arduino tools drop-down.Typically, only one number following `usbmodem`
      will change. 
   3. Open `mainprogram.py` and go to line 503. Change the serial port number to 
      match the one the device is currently connected to, as seen in the 
      arduino tools drop-down.Typically, only one number following `usbmodem`
      will change.
5. Manual setup of software is now complete!

## Device User Manual
1. To start the GUI, type `welcomepage.py`
   on the command line, or load and run `welcomepage.py` in the IDE
   of your choice. Make sure the device is powered on (yellow LED indicator on
   side of box should be on)
2. The GUI window "Welcome" should then display.
3. Press the next button to continue.
4. The Calibration page should then display. Press the calibration button on 
   the side of the box, as instructed to by the screen. The blue indicator LED
   light should then turn on. The screen will then display "WAIT", and then
   instruct the user (both visually and with auditory cues) to breath in and out
   six times as the device calibrates. When finished, the screen will inform 
   the user calibration is complete. 
5. Press the next button to continue.
6. The Menu page of the GUI will then display. Read the instructions at the top
of the page to acquaint yourself with the breathing instruction color codes.
7. Press the choose song button. Choose between billiejean and icanfly for your
breathing audio entertainment!
8. Enter the current user's name in the "Patient Name" entry box.
9. Enter the desired length of breath in seconds for this session in the 
   "Desired Length of Breath" entry box.
9. Pick a desired inhale and exhale threshold (1-3) from the corresponding 
dropdown menus "Great Inhale Threshold" and "Great Exhale Threshold". NOTE: Bypassing
   this step will result in an error. 
10. Pick a desired resistance level (0-5) from the corresponding 
dropdown menu "Resistance Level". Make sure to match this setting to whatever 
    you have turned the mechanical device's resistance knob to!
11. Press the end session button to quit the program, if desired.  
11. If not, press the next button to continue.
12. A warning popup will occur asking if you have set the resistance level. 
13. If you press no, you will return to the menu page, and should enter the 
resistance level at this time.
14. If you press yes, the main page of the GUI will then display. 
15. Press the start button to begin your breathing training session!
    1. Your song of choice will begin to play with a metronome overlayed. 
       Breathing instructions will appear below the main graph. The dot with a 
       bright red box around it is the dot you should be watching for instruction. 
       You will see your breaths in real time on the main graph. 
    2. You will receive a "Great Inhale!" popup message in the top right corner
       of the screen if your breath goes above the great inhale threshold line, 
       and you will receive a "Great Exhale!" popup message in the top right corner
       of the screen if your breath goes below the great exhale threshold line.
       This is your goal!
16. Press the cancel button to return to the menu page. 
17. Press the pause button to pause the song and both moving graphs. 
18. Press the End Session button if you wish to end the session. 
19. This will stop the song and moving graphs, and take you to a Summary
Metrics page. 
    1. This Summary page displays metrics describing your session.
20. Press the Save As... button to open a popup to save a file of data containing
your summary messages. You will be able to enter the name and location of the 
    file you are saving.
21. Press the cancel button to return to the main page. 
22. Press the restart button to return to the menu page.

## License
MIT License

Copyright (c) 2021 Haley Elena Snyder

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

       
    
