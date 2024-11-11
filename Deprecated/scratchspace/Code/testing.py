from psychopy import visual, core
from parameters import Parameters
from trial import TrustGameTrial
from markEvent import markEvent
from Class.game_logic import GameLogic
from stimuli import create_image_stimuli  # Import for loading images
import globals as glb

def run_experiment_test():
    # Initialize parameters and global settings
    PARAMETERS = Parameters()
    UI_WIN = PARAMETERS.create_window()  # Create a PsychoPy window based on PARAMETERS

    all_data = []
    trial_counter = 0

    # Mark the start of the experiment
    markEvent("taskStart", PARAMETERS=PARAMETERS)
    
    # Main experiment loop for each block in PARAMETERS.blocks
    for block_idx, block in enumerate(PARAMETERS.blocks):
        # Initialize GameLogic for this block with specified trustworthiness
        game_logic = GameLogic(
            UI_WIN=UI_WIN,
            parameters=PARAMETERS,
            trustworthiness=block['trustworthiness'],
            initial_money=1,
            user_role="trustor",   # Set user role for this block
            cpu_role="trustee"     # Set CPU role for this block
        )
        
        # Load partner image for all trials in this block
        partner_image = create_image_stimuli(UI_WIN, PARAMETERS.stimuli['imageFolder'])

        # Initialize the trial with the user as trustor and CPU as trustee
        trial = TrustGameTrial(
            UI_WIN=UI_WIN,
            PARAMETERS=PARAMETERS,
            partner_name=block['name'],
            game_logic=game_logic,
            user_role="trustor",
            cpu_role="trustee",
            trialIdx=0,
            blockIdx=block_idx,
            partner_image=partner_image,  # Pass the loaded image here
            block_image=None  # Placeholder if additional block image needed
        )
        
        # Show introductory screen for the block
        trial.show_intro()  # Display partner's name and image for introduction


    # Mark the end of the experiment
    markEvent("taskStop", PARAMETERS=PARAMETERS)
   