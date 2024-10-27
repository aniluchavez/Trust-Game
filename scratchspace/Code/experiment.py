import pandas as pd
from psychopy import visual, core
from Class.game_logic import GameLogic
from markEvent import markEvent
from Code.trial import TrustGameTrial  # Assuming the trial script is named trial.py
import Code.globals as glb
import random

def run_experiment(TaskVars, PARAMETERS):
    """
    Main function to run the experiment. Initializes blocks and trials, assigns roles, and saves data.
    
    Parameters:
    ----------
    TaskVars : dict
        A dictionary containing prompts and experimental conditions.
    PARAMETERS : dict
        A dictionary containing experimental settings, including block and trial information.
    """
    # Initialize PsychoPy window
    UI_WIN = visual.Window([1024, 768], fullscr=False, units='pix')
    all_data = []  # Collect data for the entire experiment
    
    # Mark the start of the experiment
    markEvent("taskStart")
    
    # Loop through each block
    for blockIdx in range(PARAMETERS['exp']['numBlocks']):
        block_data = []
        prompts = TaskVars['prompts']
        
        # Shuffle prompts at the start of each block
        random.shuffle(prompts)

        # Assign roles based on block configuration (e.g., alternate trustor and trustee roles)
        user_role = 'trustor' if blockIdx % 2 == 0 else 'trustee'
        cpu_role = 'trustee' if user_role == 'trustor' else 'trustor'

        # Mark the start of the block
        markEvent('blockStart', blockIdx + 1)
        
        # Initialize game logic with the current role setup and parameters
        game_logic = GameLogic(UI_WIN, trustworthiness='trustworthy', initial_money=3)

        # Loop through each trial within the block
        for trialIdx in range(PARAMETERS['block']['numTrials']):
            # Create and run trial
            trial = TrustGameTrial(
                UI_WIN=UI_WIN,
                PARAMETERS=PARAMETERS,
                partner_name="Chris Thompson",  # Example partner name
                partner_image_folder="/path/to/images",
                num_images=1,
                game_logic=game_logic,
                user_role=user_role,
                cpu_role=cpu_role,
                trialIdx=trialIdx,
                blockIdx=blockIdx
            )
            outcome = trial.run_trial()

            # Collect trial data
            trial_data = {
                'Trial Index': trialIdx,
                'Block Index': blockIdx,
                'User Role': user_role,
                'Outcome': outcome,  # The outcome returned from trial
                'Prompt': prompts[trialIdx]
            }
            all_data.append(trial_data)
            block_data.append(trial_data)

            # Check if the trial or block was aborted
            if outcome.get('Abort'):
                break
        
        # Save block data to a separate file
        pd.DataFrame(block_data).to_excel(PARAMETERS['outputDir'] + f'Block_{blockIdx + 1}.xlsx')
        
        # Mark the end of the block
        markEvent('blockEnd', blockIdx + 1)
        
        # Exit experiment if an abort was triggered during the block
        if outcome.get('Abort'):
            markEvent("taskAbort")
            break

    # Save all experiment data after completing all blocks
    pd.DataFrame(all_data).to_excel(PARAMETERS['outputDir'] + 'Behavioral_Data.xlsx')

    # Mark the end of the experiment
    markEvent("taskStop")
    UI_WIN.close()
    core.quit()
