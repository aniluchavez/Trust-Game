from psychopy import core
from markEvent import markEvent
from trial import TrustGameTrial
from Class.game_logic import GameLogic
from stimuli import load_partner_image
import globals as glb

def run_experiment():
    PARAMETERS = glb.PARAMETERS
    UI_WIN = PARAMETERS.create_window()
    all_data = []

    # Show welcome screen
    welcome_trial = TrustGameTrial(
        UI_WIN=UI_WIN,
        PARAMETERS=PARAMETERS,
        partner_name="",
        game_logic=None,
        user_role="trustor",
        cpu_role="trustee",
        trialIdx=0,
        blockIdx=0
    )
    welcome_trial.show_welcome()

    for block_idx, block in enumerate(PARAMETERS.blocks):
        # Block setup (roles, partner image, etc.)
        user_role = block.get('user_role', 'trustor')
        cpu_role = 'trustee' if user_role == 'trustor' else 'trustor'
        game_logic = GameLogic(
            PARAMETERS=PARAMETERS,
            trustworthiness=block['trustworthiness'],
            initial_money=1
        )
        partner_image = load_partner_image(UI_WIN, PARAMETERS.stimuli['imageFolder'])

        # Run trials for the block
        for trial_idx in range(block['num_trials']):
            trial_user_role = 'trustor' if trial_idx % 2 == 0 else 'trustee' if block.get('alternate_roles', False) else user_role
            trial_cpu_role = 'trustee' if trial_user_role == 'trustor' else 'trustor'
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
            trial_data = trial.run_trial()

            # Capture initial ranking from the first trial
            if trial_idx == 0:
                trial_data["initial_ranking"] = trial.trust_slider.getRating() or 5

            all_data.append(trial_data)

        # End-of-block trust rating
        block_end_trial = TrustGameTrial(
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
        end_block_ranking = block_end_trial.show_block_ranking()
        all_data.append({"blockIdx": block_idx, "end_block_ranking": end_block_ranking})

    markEvent("taskStop", PARAMETERS=PARAMETERS)
    save_data(all_data)
    UI_WIN.close()

def save_data(data_records, filename="experiment_data"):
    import csv, os
    filepath = os.path.join(glb.DATA_PATH, f"{filename}.csv")
    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data_records[0].keys())
        writer.writeheader()
        writer.writerows(data_records)
