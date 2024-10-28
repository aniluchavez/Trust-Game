from psychopy import core, visual
from markEvent import markEvent
from trial import TrustGameTrial
from Class.game_logic import GameLogic
from stimuli import load_partner_image
import globals as glb

def run_experiment():
    """
    Main function to run the trust game experiment.
    Initializes game logic, displays intro, and loops through trials in each block.
    """
    PARAMETERS = glb.PARAMETERS  # Access PARAMETERS from globals
    UI_WIN = PARAMETERS.create_window()
    all_data = []  # To store data across all trials

    # Mark the start of the experiment
    markEvent("taskStart", PARAMETERS=PARAMETERS)

    # Main loop through blocks in PARAMETERS
    for block_idx, block in enumerate(PARAMETERS.blocks):
    # Set roles from block settings or defaults
        user_role = block.get('user_role', 'trustor')
        cpu_role = block.get('cpu_role', 'trustee')
        
        # Initialize GameLogic for the block
        game_logic = GameLogic(
            PARAMETERS=PARAMETERS,
            trustworthiness=block['trustworthiness'],
            initial_money=1
        )

        # Load partner image for the block
        partner_image = load_partner_image(UI_WIN, PARAMETERS.stimuli['imageFolder'])

        # Initialize trial with specified roles
        trial = TrustGameTrial(
            UI_WIN=UI_WIN,
            PARAMETERS=PARAMETERS,
            partner_name=block['name'],
            game_logic=game_logic,
            user_role=user_role,
            cpu_role=cpu_role,
            trialIdx=0,
            blockIdx=block_idx,
            partner_image=partner_image
        )

    # Run block introduction and trials
        trial.show_intro()
        for trial_idx in range(block['num_trials']):
            trial.trialIdx = trial_idx
            trial_data = trial.run_trial()
            all_data.append(trial_data)

    # Mark the end of the experiment
    markEvent("taskStop", PARAMETERS=PARAMETERS)

    # Save all collected data at the end
    save_data(all_data)

def save_data(data_records, filename="experiment_data"):
    """
    Save experiment data to a CSV file.

    Parameters:
    ----------
    data_records : list of dict
        Collected data for each trial.
    filename : str
        Base filename for saving data.
    """
    import csv, os
    filepath = os.path.join(glb.DATA_PATH, f"{filename}.csv")

    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data_records[0].keys())
        writer.writeheader()
        writer.writerows(data_records)
