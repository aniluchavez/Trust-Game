# parameters.py
from psychopy import core, gui, data, prefs, visual
from numpy.random import randint
import os

# --- Set hardware preferences ---
prefs.hardware['audioLib'] = ['sounddevice', 'pygame']
prefs.hardware['audioLatencyMode'] = '3'

class Parameters:
    def __init__(self):
        # Screen, text, and window configurations
        self.screen = {'number': 1, 'bgColor': [0.5, 0.5, 0.5]}
        self.text = {'font': 'Arial', 'size': 24, 'color': [1, 1, 1]} #[255, 255, 255]
        self.window = {'size': [1024, 768], 'fullscr': False, 'units': 'pix'}
        
        # Experiment structure and timing settings
        self.exp = {'numBlocks': 2, 'outputDir': '/path/to/output/'}
        self.block = {'numTrials': 24}
        self.timing = {'decisionDuration': 3, 'intervalDuration': 12, 'outcomeDuration': 1}
        
        # Image and stimuli settings
        self.stimuli = {
            "imageFolder": "/Users/aniluchavez/Documents/GitHub/Scratch/scratchspace/Images/CFD-MR", 
             #/Users/aniluchavez/Documents/GitHub/Scratch/scratchspace/Images/CFD-MR # Full path to the image folder 
            'numImages': 2,  # Default number of images to select
            'sliderLabels': ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        }
        self.blocks = [
            {"name": "John Pork", "image_folder": self.stimuli['imageFolder'], "num_trials": 24, "trustworthiness": "trustworthy"},
            {"name": "Daquavius Pork", "image_folder": self.stimuli['imageFolder'], "num_trials": 24, "trustworthiness": "untrustworthy"},
            # Add additional blocks as needed
        ]
        self.trustworthy_weights = {'low': 0.2, 'high': 0.8}      # Trustworthy behavior weights
        self.untrustworthy_weights = {'low': 0.8, 'high': 0.2} 
        self.events = []
        # Global clocks and save data placeholders
        self.REL_CLOCK = core.Clock()
        self.ABS_CLOCK = core.Clock()
        self.SAVE_DATA = []
        
    def show_exp_info(self):
        """Shows dialog box to collect participant info."""
        expInfo = {
            'participant': f"{randint(0, 999999):06.0f}",
            'session': '001',
            'date': data.getDateStr(),
            'expName': 'trust_game',
            'psychopyVersion': '2024.2.1',
        }
        
        dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expInfo['expName'], alwaysOnTop=True)
        if dlg.OK == False:
            core.quit()
        return expInfo

    def create_window(self):
        """Creates the PsychoPy window with parameters from the configuration."""
        self.UI_WIN = visual.Window(
            size=self.window['size'],
            fullscr=self.window['fullscr'],
            units=self.window['units'],
            color=self.screen['bgColor'],
            colorSpace='rgb',
        )
        return self.UI_WIN
