# Smartcard measurement scripts in Python
Should work on Windows, Linux.

Requirements:
* Python >= 3.6
* Oscilloscope control: pip install pyvisa pyvisa-py pyusb
  * User installable
* Smartcard control: pip install pyscard
  * Needs [Swig](http://www.swig.org/download.html) in PATH for the installation

Contains:
* measurement.py: Main script. Modify as needed.
* oscilloscope.py: Oscilloscope control. Uses pyvisa. 
* card.py: Smartcard control. Uses pyscard.

(c) 2022 Jiri Bucek using code by Marina Shchavleva and Filip Kodytek