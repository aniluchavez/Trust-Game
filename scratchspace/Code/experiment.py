# experiment.py
from psychopy import core, visual
from markEvent import markEvent
from trial import TrustGameTrial
from Class.game_logic import GameLogic
from stimuli import load_partner_image
import globals as glb

def run_experiment():
    PARAMETERS = glb.PARAMETERS  # Access PARAMETERS from globals
    UI_WIN = PARAMETERS.create_window()
    all_data = []  # To store data across all trials

    # Mark the start of the experiment
    markEvent("taskStart", PARAMETERS=PARAMETERS)

    # Iterate through each block in the experiment
    for block_idx, block in enumerate(PARAMETERS.blocks):
        # Define user and CPU roles for this block
        user_role = block.get('user_role', 'trustor')
        cpu_role = 'trustee' if user_role == 'trustor' else 'trustor'
        
        # Initialize GameLogic for each block with specified trustworthiness and initial money
        game_logic = GameLogic(
            PARAMETERS=PARAMETERS,
            trustworthiness=block['trustworthiness'],
            initial_money=1
        )

        # Load the partner's image for this block
        partner_image = load_partner_image(UI_WIN, PARAMETERS.stimuli['imageFolder'])

        # Introductory phase (shown once per block)
        intro_trial = TrustGameTrial(
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
        intro_trial.show_intro()

        # Trial loop within each block
        for trial_idx in range(block['num_trials']):
            # Optionally alternate roles within trials if specified
            if block.get('alternate_roles', False):
                trial_user_role = 'trustor' if trial_idx % 2 == 0 else 'trustee'
                trial_cpu_role = 'trustee' if trial_user_role == 'trustor' else 'trustor'
            else:
                trial_user_role = user_role
                trial_cpu_role = cpu_role

            # Run each trial
            trial = TrustGameTrial(
                UI_WIN=UI_WIN,
                PARAMETERS=PARAMETERS,
                partner_name=block['name'],
                game_logic=game_logic,
                user_role=trial_user_role,
                cpu_role=trial_cpu_role,
                trialIdx=trial_idx,
                blockIdx=block_idx,
                partner_image=partner_image
            )
            trial_data = trial.run_trial()  # Execute the trial
            all_data.append(trial_data)  # Collect trial data

    # Mark the end of the experiment
    markEvent("taskStop", PARAMETERS=PARAMETERS)

    # Save all collected trial data
    save_data(all_data)

def save_data(data_records, filename="experiment_data"):
    """Save collected data to a CSV file."""
    import csv, os
    filepath = os.path.join(glb.DATA_PATH, f"{filename}.csv")
    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data_records[0].keys())
        writer.writeheader()
        writer.writerows(data_records)
