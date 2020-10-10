from __future__ import print_function

import time
import logging
import sys
import string

from rtmidi.midiutil import open_midiinput
from pyautogui import press, typewrite, hotkey


log = logging.getLogger('midiin_poll')
logging.basicConfig(level=logging.DEBUG)

# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

NOTE_START = 26  # 41
NOTE_END = 56    # 71 

NOTE_PRESS = 144
SUS_PRESS = 177

ESC_KEY = 24    # 39 
CTL_KEY = 25    # 40 
RETURN_KEY = 57 # 72
DELETE_KEY = 58 # 73
TAB_KEY = 59 # 74
SHIFT_KEY = 60

ALPHA = "sxrcwvaezqdftg yuhkjilobnpm/:=."
DIGITS = string.digits


print("Entering main loop. Press Control-C to exit.")
try:
    shift_is_pressed = False
    ctl_is_pressed = False

    while True:
        msg = midiin.get_message()
      
        if msg:
	    key_type = msg[0][0]
            note = msg[0][1]
            print("MSG:", msg, "NOTE: ", note)
	    print("---")


            # note_press on 
	    if msg[0][2]:
              if key_type == SUS_PRESS or key_type == SUS_PRESS-1 or note == SHIFT_KEY:
                shift_is_pressed = True
	      # check if alpha
	      elif note >= NOTE_START and note <= NOTE_END:
                note = note - NOTE_START 
		key = ALPHA[note]
	        if shift_is_pressed:
                  key = key.upper()
	        if ctl_is_pressed:
	          hotkey('ctl', key)
		else:
		  press(key)
	      elif note == CTL_KEY:
                ctl_is_pressed = True
	      elif note == RETURN_KEY:
	        press('enter')
	      elif note == DELETE_KEY:
	        press('backspace')
	      elif note == TAB_KEY:
	        press('tab')
	    else:
             if key_type == SUS_PRESS or key_type == SUS_PRESS-1 or note == SHIFT_KEY:
               shift_is_pressed = False 
	     if note == CTL_KEY:
               ctl_is_pressed = False 

        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin



# import keyboard 
# keyboard.write('the quick brown fox jumps over the lazy dog.')
