from psychopy import locale_setup, prefs, core, gui, visual, data, clock, hardware
from psychopy.tools import environmenttools
from numpy.random import randint
import os

# --- Set hardware preferences ---
prefs.hardware['audioLib'] = ['sounddevice', 'pygame']
prefs.hardware['audioLatencyMode'] = '3'

# ParameterClass for experiment settings, you can also create more parameters outside in a different file @George this is similar
# to your parameterclass.py
class ParameterClass:
    def __init__(self):
        self.screen = {'number': 1, 'bgColor': [0, 0, 0]}
        self.text = {'font': 'Arial', 'size': 24, 'color': [255, 255, 255]}
        self.window = {'size': [1024, 768], 'fullscr': False, 'units': 'pix'}

# --- Create global variables ---
def create_globals():
    global PARAMETERS
    PARAMETERS = ParameterClass()  # Load all parameters in a single class

    global REL_CLOCK, ABS_CLOCK
    REL_CLOCK = core.Clock()  # relative clock
    ABS_CLOCK = core.Clock()  # absolute clock

    global UI_WIN
    UI_WIN = visual.Window(PARAMETERS.window['size'], fullscr=PARAMETERS.window['fullscr'],
                           units=PARAMETERS.window['units'], colorSpace='rgb255',
                           color=PARAMETERS.screen['bgColor'])

    global SAVE_DATA
    SAVE_DATA = []

# --- Function to show participant info dialog ---
def showExpInfoDlg():
    expInfo = {
        'participant': f"{randint(0, 999999):06.0f}",
        'session': '001',
        'date': data.getDateStr(),
        'expName': 'testing',
        'psychopyVersion': '2024.2.1',
    }
    
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expInfo['expName'], alwaysOnTop=True)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    return expInfo

# --- Function to create visual stimuli ---
#def create_stimuli():
    # global UI_TEXT, UI_RECT
    
    # UI_TEXT = visual.TextStim(UI_WIN, text='Welcome', font=PARAMETERS.text['font'],
    #                           color=PARAMETERS.text['color'], height=PARAMETERS.text['size'])

    #UI_RECT = visual.Rect(UI_WIN, width=200, height=200, fillColor=[255, 0, 0])

# --- Main function to run the experiment --- this can exist somewhere else, but for now it will go here 
# def run_experiment():
#     create_globals()  # Initialize global variables and clocks
#     expInfo = showExpInfoDlg()  # Show participant info dialog
#     create_stimuli()  # Create all stimuli

#     # Now the experiment can begin
#     UI_TEXT.draw()  # Display text stimulus
#     UI_WIN.flip()  # Refresh the window to display the stimulus

#     core.wait(2)  # Wait for 2 seconds
#     #UI_RECT.draw()  # Display rectangle stimulus
#     #UI_WIN.flip()  # Refresh the window to display the stimulus

#     #core.wait(2)  # Wait for 2 seconds before ending the experiment

# if __name__ == '__main__':
#     run_experiment()
