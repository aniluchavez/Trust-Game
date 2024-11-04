import random, os
from numpy.random import randint
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox as tkm

from psychopy import core, gui, data, prefs, visual, monitors

# Set hardware preferences for PsychoPy
prefs.hardware['audioLib'] = ['sounddevice', 'pygame']
prefs.hardware['audioLatencyMode'] = '3'

class Parameters:
    def __init__(self):
        # Screen, text, and window configurations
        self.screen = {'number': 1, 'fullscr': True}
        self.window = {'size': [1024, 768], 'bgColor': [90,90,90], 'units': 'norm'}
        
        self.text = {'font': 'Arial', 'size': 24, 'color': [255, 255, 255]}  # Simplified font to 'Arial'
        
        # Experiment structure and timing settings
        self.exp = {
            'name'     : "TrustGame",  # A name for the task to be used in filenames
            'numBlocks': 10,  # Number of blocks in the experiment
            'outputDir': 'data',  # Output directory for saving data
            'trialsPerBlock': 48
        }
        # self.block = {
        #     'numTrials': 48  # Total number of trials in each block
        # }
        self.timing = {
            'photodiode' : 0.25,
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
        self.outputDir=''
        self.ID={}
        self.__launch_ID_UI()

        # Size computation for text based on screen settings
        # self.text.update({'sizeCM': self.text['size']*0.0352777778})

    def get_block_info(self):
        """Returns the number of blocks and trials per block."""
        return self.exp['numBlocks'], self.exp['trialsPerBlock'] #self.block['numTrials']

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
            remaining_blocks = self.exp['numBlocks'] - (block_idx + 1)
            shortfall = self.exp['trialsPerBlock'] * self.exp['numBlocks'] - (3 + self.exp['trialsPerBlock'] * remaining_blocks)  # Expected 120 total for each type minus what Block 1 contributed
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
    
    def generate_output_dest(self):
        # Generate dynamic strings
        now:str = datetime.now().strftime("%Y%m%d_%H%M") 
        idName= self.ID['name']
        expName= self.exp['name']
        userPath = os.path.expanduser('~')
        
        # Generate the directories needed for the outputdirectory
        outputDir = f'{userPath}/Documents/PatientData'
        if not os.path.exists(outputDir): os.mkdir(outputDir)

        outputDir += f'/{idName}'
        if not os.path.exists(outputDir): os.mkdir(outputDir)

        outputDir += f'/{expName}'
        if not os.path.exists(outputDir): os.mkdir(outputDir)
    
        self.outputDir = outputDir + f'/{expName}__{idName}_{now}/'
        if not os.path.exists(self.outputDir): os.mkdir(self.outputDir)
    

    def __launch_ID_UI(self):
        idUI = tk.Tk() 
        idUI.title('ID specifications')
        rowNum = 0

        # Label text for Name
        nameLabel = ttk.Label(idUI, text = "Please enter the participant's name/refID:")
        nameLabel.grid(row =rowNum, column=1, padx=10, sticky='W')
        rowNum += 1

        # Text Box for the Name
        nameEntry = ttk.Entry(idUI, textvariable=tk.StringVar(), justify=tk.LEFT)
        nameEntry.insert(0, 'TEST')
        nameEntry.grid(row=rowNum, column=1, padx=10, sticky='W')
        rowNum += 1

        # Blank Space
        ttk.Label(idUI).grid(row =rowNum, column=1)
        rowNum += 1

        # Label for exp Env Option
        expEnvLabel = ttk.Label(idUI, text='Select Experimental Setup:')
        expEnvLabel.grid(row=rowNum, column=1, padx=10, sticky='W')
        rowNum += 1

        # Combobox creation 
        expEnvList = ttk.Combobox(idUI, width = 20, textvariable = tk.StringVar()) 
        expEnvList['values'] = ('None', 'BCM-EMU') 
        expEnvList.grid(row=rowNum, column=1, padx=10, sticky='W') 
        expEnvList.current() 
        rowNum += 1

        # Blank Space
        ttk.Label(idUI).grid(row =rowNum, column=1)
        rowNum += 1

        def save_button():
            self.ID.update({'name': nameEntry.get(),
                            'expEnv': expEnvList.get()})
            shouldDestroy = True
            for key in self.ID.keys():
                if self.ID[key] == '': shouldDestroy = False

            if self.ID['expEnv'] not in expEnvList['values']:
                shouldDestroy = False

            if shouldDestroy:
                idUI.destroy()
            else:
                tkm.showwarning(title='Incorrect values', message='Some of the values appear to be missing or incorrect')
            
        saveButton = ttk.Button(idUI, text='Save', command=save_button)
        saveButton.grid(row=rowNum, column = 1)
        idUI.mainloop() 

