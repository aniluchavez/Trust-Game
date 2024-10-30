from psychopy import core, gui, data, prefs, visual, monitors
from numpy.random import randint
import os
import random

# Set hardware preferences for PsychoPy
prefs.hardware['audioLib'] = ['sounddevice', 'pygame']
prefs.hardware['audioLatencyMode'] = '3'

class Parameters:
    def __init__(self):
        # Screen, text, and window configurations
        self.screen = {'number': 1, 'bgColor': [0.5, 0.5, 0.5]}
        self.text = {'font': 'Arial', 'size': 24, 'color': [1, 1, 1]}  # Simplified font to 'Arial'
        self.window = {'size': [1024, 768], 'fullscr': False, 'units': 'norm'}

        self.monitor = monitors.Monitor(name='testMonitor', width=30.0, distance=60.0)
        self.monitor.setSizePix([1024, 768])

        # Experiment structure and timing settings
        self.exp = {
            'numBlocks': 2,  # Number of blocks in the experiment
            'outputDir': 'data'  # Output directory for saving data
        }
        self.block = {
            'numTrials': 24  # Total number of trials in each block
        }
        self.timing = {
            'decisionDuration': 3,  # Decision phase duration (in seconds)
            'intervalDuration': 12,  # Interval between decision and outcome
            'outcomeDuration': 1  # Outcome display duration
        }

        # Image and stimuli settings
        self.stimuli = {
            "imageFolder": "Images/CFD-MR",  # Generic path to the folder containing images
            'numImages': 2,
            'sliderLabels': ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        }
        self.lottery_ratio = 0.1
        # Trustworthiness weights, customizable for each partner in a block
        self.trustworthy_weights = {'low': 0.2, 'high': 0.8}
        self.untrustworthy_weights = {'low': 0.8, 'high': 0.2}

        # Define interleaved blocks with equal sampling configuration for trials
        self.blocks = [
            {
                "partners": [
                    {"name": "Kendall Christie", "image": "CFD-MF-300-002-N.jpg", "trustworthiness": "trustworthy", "weights": self.trustworthy_weights},
                    {"name": "Alex Smith", "image": "CFD-MM-302-010-N.jpg", "trustworthiness": "untrustworthy", "weights": self.untrustworthy_weights}
                ],
                "num_trials_per_partner": 12  # Total trials per partner per block (for interleaving)
            },
            {
                "partners": [
                    {"name": "Michael Ham", "image": "CFD-MF-329-003-N.jpg", "trustworthiness": "trustworthy", "weights": {"low": 0.3, "high": 0.7}},
                    {"name": "Chad Bacon", "image": "CFD-MM-311-007-N.jpg", "trustworthiness": "untrustworthy", "weights": {"low": 0.7, "high": 0.3}}
                ],
                "num_trials_per_partner": 12  # Customize trial count if required
            }
        ]

        # Global clocks and data storage
        self.REL_CLOCK = core.Clock()
        self.ABS_CLOCK = core.Clock()
        self.SAVE_DATA = []
        
        # Initialize events list to store experiment events
        self.events = []

    def get_block_info(self):
        """Returns the number of blocks and trials per block."""
        return self.exp['numBlocks'], self.block['numTrials']

    def get_interleaved_trial_types(self, num_trials):
        """
        Returns a balanced list of trial types for a block (half trust trials, half lottery trials).
        Ensures equal representation of trial types within each block.
        """
        num_lottery_trials = int(num_trials * self.lottery_ratio)
        num_trust_trials = num_trials - num_lottery_trials

        trial_types = ['lottery'] * num_lottery_trials + ['trust'] * num_trust_trials
        random.shuffle(trial_types)  # Shuffle to interleave trial types
        return trial_types

    def get_block_partners(self, block_idx):
        """Returns the partner configurations for the specified block index."""
        return self.blocks[block_idx]["partners"]
    
    def get_selected_partners(self, num_partners=2):
        """Return the first `num_partners` partners in each block for simplicity."""
        selected_partners = []
        for block in self.blocks:
            selected_partners.append({
                "partners": block["partners"][:num_partners],
                "num_trials_per_partner": block["num_trials_per_partner"]
            })
        return selected_partners
    
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
        """Creates the PsychoPy window with consistent parameters."""
        self.UI_WIN = visual.Window(
            size=self.window['size'],
            fullscr=self.window['fullscr'],
            units=self.window['units'],
            color=self.screen['bgColor'],
            colorSpace='rgb',
            monitor=self.monitor  # Using explicit monitor settings
        )
        return self.UI_WIN
