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
        self.screen = {'number': 1, 'fullscr': True}
        self.window = {'size': [1024, 768], 'bgColor': [122,122,122], 'units': 'norm'}
        
        self.text = {'font': 'Arial', 'size': 24, 'color': [255, 255, 255]}  # Simplified font to 'Arial'
        
        # Experiment structure and timing settings
        self.exp = {
            'numBlocks': 10,  # Increase number of blocks to 10
            'outputDir': 'data'  # Output directory for saving data
        }
        self.block = {
            'numTrials': 48  # Total number of trials in each block
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
        self.lottery_ratio = 0.1  # For initial downsampling in the first block
        # Trustworthiness weights for each CPU type
        self.trustworthy_weights = {'low': 0.2, 'high': 0.8}
        self.untrustworthy_weights = {'low': 0.8, 'high': 0.2}

        # CPU partner configuration - consistent across all blocks
        self.partners = [
            {"name": "Kendall Christie", "image": "CFD-MF-300-002-N.jpg", "trustworthiness": "trustworthy", "weights": self.trustworthy_weights},
            {"name": "Alex Smith", "image": "CFD-MM-321-021-N.jpg", "trustworthiness": "untrustworthy", "weights": self.untrustworthy_weights},
            {"name": "Taylor Reed", "image": "CFD-MF-306-003-N.jpg", "trustworthiness": "neutral", "weights": None}  # Neutral partner, no weights
        ]

        # Size computation for text based on screen settings
        self.text.update({'sizeCM': self.text['size']*0.0352777778})

    def get_block_info(self):
        """Returns the number of blocks and trials per block."""
        return self.exp['numBlocks'], self.block['numTrials']

    def get_interleaved_trial_types(self, num_trials, block_idx):
        """
        Returns a balanced list of trial types for each block, adjusting the first block to under-sample lottery trials
        and compensating in subsequent blocks to reach equal totals of 120 trials for each type by the end.
        """
        # Calculate target number of lottery trials for the first block
        if block_idx == 0:
            num_lottery_trials = 3  # Fewer lottery trials in Block 1
        else:
            # Adjust lottery count slightly in subsequent blocks to compensate
            remaining_blocks = 10 - (block_idx + 1)
            shortfall = 24 * 10 - (3 + 24 * remaining_blocks)  # Expected 120 total for each type minus what Block 1 contributed
            num_lottery_trials = (num_trials // 2) + (shortfall // remaining_blocks)

        # Calculate trust trials to balance the block
        num_trust_trials = num_trials - num_lottery_trials

        # Create the list and shuffle to interleave
        trial_types = ['lottery'] * num_lottery_trials + ['trust'] * num_trust_trials
        random.shuffle(trial_types)  # Shuffle for interleaving
        return trial_types


    def get_block_partners(self, block_idx):
        """Returns the partner configurations for any block index (same partners for all blocks)."""
        return self.partners
    
    def get_selected_partners(self, num_partners=2):
        """Return the first `num_partners` partners in each block for simplicity."""
        return {
            "partners": self.partners[:num_partners],
            "num_trials_per_partner": self.block['numTrials'] // len(self.partners)
        }
    
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





# from psychopy import core, gui, data, prefs, visual, monitors
# from numpy.random import randint
# import os
# import random

# # Set hardware preferences for PsychoPy
# prefs.hardware['audioLib'] = ['sounddevice', 'pygame']
# prefs.hardware['audioLatencyMode'] = '3'

# class Parameters:
#     def __init__(self):
#         # Screen, text, and window configurations
#         self.screen = {'number': 1, 'fullscr': True}
#         self.window = {'size': [1024, 768], 'bgColor': [122,122,122], 'units': 'norm'}
        
#         self.text = {'font': 'Arial', 'size': 24, 'color': [255, 255, 255]}  # Simplified font to 'Arial'
        
#         # Experiment structure and timing settings
#         self.exp = {
#             'numBlocks': 8,  # Number of blocks in the experiment
#             'outputDir': 'data'  # Output directory for saving data
#         }
#         self.block = {
#             'numTrials': 24  # Total number of trials in each block
#         }
#         self.timing = {
#             'decisionDuration': 3,  # Decision phase duration (in seconds)
#             'intervalDuration': 12,  # Interval between decision and outcome
#             'outcomeDuration': 1  # Outcome display duration
#         }

#         # Image and stimuli settings
#         self.stimuli = {
#             "imageFolder": "Images/CFD-MR",  # Generic path to the folder containing images
#             'numImages': 2,
#             'sliderLabels': ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
#         }
#         self.lottery_ratio = 0.1
#         # Trustworthiness weights, customizable for each partner in a block
#         self.trustworthy_weights = {'low': 0.2, 'high': 0.8}
#         self.untrustworthy_weights = {'low': 0.8, 'high': 0.2}

#         # Define interleaved blocks with partners, including a neutral partner with no weights
#         self.blocks = [
#             {
#                 "partners": [
#                     {"name": "Kendall Christie", "image": "CFD-MF-300-002-N.jpg", "trustworthiness": "trustworthy", "weights": self.trustworthy_weights},
#                     {"name": "Alex Smith", "image": "CFD-MM-321-021-N.jpg", "trustworthiness": "untrustworthy", "weights": self.untrustworthy_weights},
#                     {"name": "Taylor Reed", "image": "CFD-MF-306-003-N.jpg", "trustworthiness": "neutral", "weights": None}  # Neutral partner, no weights
#                 ],
#                 "num_trials_per_partner": 12  # Total trials per partner per block (for interleaving)
#             },
#             {
#                 "partners": [
#                     {"name": "Michael Ham", "image": "CFD-MF-329-001-N.jpg", "trustworthiness": "trustworthy", "weights": {"low": 0.3, "high": 0.7}},
#                     {"name": "Chad Bacon", "image": "CFD-MM-311-001-N.jpg", "trustworthiness": "untrustworthy", "weights": {"low": 0.7, "high": 0.3}},
#                     {"name": "Jamie Lee", "image": "CFD-MM-313-001-N.jpg", "trustworthiness": "neutral", "weights": None}  # Another neutral partner
#                 ],
#                 "num_trials_per_partner": 12  # Customize trial count if required
#             }
#         ]

#         # Size computation for text based on screen settings
#         self.text.update({'sizeCM': self.text['size']*0.0352777778})

#     def get_block_info(self):
#         """Returns the number of blocks and trials per block."""
#         return self.exp['numBlocks'], self.block['numTrials']

#     def get_interleaved_trial_types(self, num_trials):
#         """
#         Returns a balanced list of trial types for a block (half trust trials, half lottery trials).
#         Ensures equal representation of trial types within each block.
#         """
#         num_lottery_trials = int(num_trials * self.lottery_ratio)
#         num_trust_trials = num_trials - num_lottery_trials

#         trial_types = ['lottery'] * num_lottery_trials + ['trust'] * num_trust_trials
#         random.shuffle(trial_types)  # Shuffle to interleave trial types
#         return trial_types

#     def get_block_partners(self, block_idx):
#         """Returns the partner configurations for the specified block index."""
#         return self.blocks[block_idx]["partners"]
    
#     def get_selected_partners(self, num_partners=2):
#         """Return the first `num_partners` partners in each block for simplicity."""
#         selected_partners = []
#         for block in self.blocks:
#             selected_partners.append({
#                 "partners": block["partners"][:num_partners],
#                 "num_trials_per_partner": block["num_trials_per_partner"]
#             })
#         return selected_partners
    
#     def show_exp_info(self):
#         """Shows a dialog box for collecting participant information."""
#         expInfo = {
#             'participant': f"{randint(0, 999999):06.0f}",
#             'session': '001',
#             'date': data.getDateStr(),
#             'expName': 'trust_game',
#             'psychopyVersion': '2024.2.1',
#         }
#         dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expInfo['expName'], alwaysOnTop=True)
#         if not dlg.OK:
#             core.quit()  # Exit if user cancels the dialog
#         return expInfo
