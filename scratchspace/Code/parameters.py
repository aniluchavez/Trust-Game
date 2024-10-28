from psychopy import core, gui, data, prefs, visual
from numpy.random import randint
import os

# Set hardware preferences for PsychoPy
prefs.hardware['audioLib'] = ['sounddevice', 'pygame']
prefs.hardware['audioLatencyMode'] = '3'

class Parameters:
    def __init__(self):
        # Screen, text, and window configurations
        self.screen = {
            'number': 1,
            'bgColor': [0.5, 0.5, 0.5]  # Gray background color
        }
        self.text = {
            'font': 'Arial',
            'size': 24,
            'color': [1, 1, 1]  # White text color in RGB format
        }
        self.window = {
            'size': [1024, 768],
            'fullscr': False,
            'units': 'pix'
        }

        # Experiment structure and timing settings
        self.exp = {
            'numBlocks': 2,  # Number of blocks in the experiment
            'outputDir': 'data'  # Output directory for saving data
        }
        self.block = {
            'numTrials': 24  # Number of trials in each block
        }
        self.timing = {
            'decisionDuration': 3,  # Decision phase duration (in seconds)
            'intervalDuration': 12,  # Interval between decision and outcome
            'outcomeDuration': 1  # Outcome display duration
        }

        # Image and stimuli settings
        self.stimuli = {
            "imageFolder": "/Users/aniluchavez/Documents/GitHub/Scratch/scratchspace/Images/CFD-MR",
            'numImages': 2,  # Number of images to select from
            'sliderLabels': ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        }

        # Define block-specific parameters (trustworthiness levels for each block)
        self.blocks = [
            {"name": "John Pork", "image_folder": self.stimuli['imageFolder'], "num_trials": 24, "trustworthiness": "trustworthy"},
            {"name": "Daquavius Pork", "image_folder": self.stimuli['imageFolder'], "num_trials": 24, "trustworthiness": "untrustworthy"},
        ]

        # Trustworthiness settings
        self.trustworthy_weights = {'low': 0.2, 'high': 0.8}
        self.untrustworthy_weights = {'low': 0.8, 'high': 0.2}

        # Global clocks and data storage
        self.REL_CLOCK = core.Clock()
        self.ABS_CLOCK = core.Clock()
        self.SAVE_DATA = []
        
        # Initialize events list to store experiment events
        self.events = []

    def show_exp_info(self):
        """Shows a dialog box for collecting participant information."""
        expInfo = {
            'participant': f"{randint(0, 999999):06.0f}",
            'session': '001',
            'date': data.getDateStr(),
            'expName': 'trust_game',
            'psychopyVersion': '2024.2.1',
        }
        dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expInfo['expName'], alwaysOnTop=True)
        if not dlg.OK:
            core.quit()  # Exit if user cancels the dialog
        return expInfo

    def create_window(self):
        """Creates the PsychoPy window based on parameters."""
        return visual.Window(
            size=self.window['size'],
            fullscr=self.window['fullscr'],
            units=self.window['units'],
            color=self.screen['bgColor'],
            colorSpace='rgb'
        )
