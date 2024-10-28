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

    for block_idx, block in enumerate(PARAMETERS.blocks):
        # Define roles for this block
        user_role = block.get('user_role', 'trustor')
        cpu_role = 'trustee' if user_role == 'trustor' else 'trustor'
        
        # Initialize GameLogic for each block
        game_logic = GameLogic(
            PARAMETERS=PARAMETERS,
            trustworthiness=block['trustworthiness'],
            initial_money=1
        )

        # Load the partner's image for the block
        partner_image = load_partner_image(UI_WIN, PARAMETERS.stimuli['imageFolder'])

        # Introduce block and partner
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
        trial.show_intro()

        # Loop through trials within the block
        for trial_idx in range(block['num_trials']):
            # Determine the role for this trial, alternating if needed
            if block.get('alternate_roles', False):
                trial_user_role = 'trustor' if trial_idx % 2 == 0 else 'trustee'
                trial_cpu_role = 'trustee' if trial_user_role == 'trustor' else 'trustor'
            else:
                trial_user_role = user_role
                trial_cpu_role = cpu_role

            # Update trial roles dynamically
            trial.user_role = trial_user_role
            trial.cpu_role = trial_cpu_role
            trial.trialIdx = trial_idx

            # Run the trial and gather data
            trial_data = trial.run_trial()
            all_data.append(trial_data)

    # Mark the end of the experiment
    markEvent("taskStop", PARAMETERS=PARAMETERS)

    # Save all collected data
    save_data(all_data)

def save_data(data_records, filename="experiment_data"):
    import csv, os
    filepath = os.path.join(glb.DATA_PATH, f"{filename}.csv")
    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data_records[0].keys())
        writer.writeheader()
        writer.writerows(data_records)
