from psychopy import core
from markEvent import markEvent
from trial import TrustGameTrial
from Class.game_logic import GameLogic
from stimuli import load_partner_image
from LotteryTrial import LotteryTrial
import globals as glb
import random

def run_experiment():
    PARAMETERS = glb.PARAMETERS
    UI_WIN = glb.UI_WIN
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
    
    # Experiment structure from parameters
    num_blocks, num_trials_per_block = PARAMETERS.get_block_info()

    # Loop through each block
    for block_idx in range(num_blocks):
        cpu_configs = PARAMETERS.get_block_partners(block_idx)

        # Initialize GameLogic with selected partners for each block
        game_logic = GameLogic(PARAMETERS, cpu_configs, initial_money=1)
        game_logic.reset_amounts()

        # Load images for each partner
        partner_images = {
            partner["name"]: load_partner_image(UI_WIN, PARAMETERS.stimuli['imageFolder'])
            for partner in cpu_configs
        }

        # Show initial trust rating for each partner only once per block
        initial_ratings = {}
        for cpu_index, partner_config in enumerate(cpu_configs):
            if partner_config["name"] not in initial_ratings:
                intro_trial = TrustGameTrial(
                    UI_WIN=UI_WIN,
                    PARAMETERS=PARAMETERS,
                    partner_name=partner_config["name"],
                    game_logic=game_logic,
                    cpu_index=cpu_index,
                    user_role="trustor",
                    cpu_role="trustee",
                    trialIdx=0,
                    blockIdx=block_idx,
                    partner_image=partner_images[partner_config["name"]]
                )
                initial_rating = intro_trial.show_intro()
                initial_ratings[partner_config["name"]] = initial_rating
                all_data.append({
                    "blockIdx": block_idx,
                    "partner": partner_config["name"],
                    "initial_rating": initial_rating
                })

        # Generate interleaved trial list using get_interleaved_trial_types only
        interleaved_trials = PARAMETERS.get_interleaved_trial_types(num_trials_per_block)
        print(f"Block {block_idx + 1} trial types:", interleaved_trials)  # Debug statement

        # Run each trial based on the interleaved structure
        for trial_idx, trial_type in enumerate(interleaved_trials):
            if trial_type == "trust":
                cpu_index, partner_config = random.choice(list(enumerate(cpu_configs)))
                trial = TrustGameTrial(
                    UI_WIN=UI_WIN,
                    PARAMETERS=PARAMETERS,
                    partner_name=partner_config["name"],
                    game_logic=game_logic,
                    cpu_index=cpu_index,
                    user_role="trustor",
                    cpu_role="trustee",
                    trialIdx=trial_idx,
                    blockIdx=block_idx,
                    partner_image=partner_images[partner_config["name"]]
                )
                trial_data = trial.run_trial()
                trial_data["initial_rating"] = initial_ratings[partner_config["name"]]
                all_data.append(trial_data)

            elif trial_type == "lottery":
                lottery_trial = LotteryTrial(UI_WIN, PARAMETERS, game_logic, list(partner_images.keys()), trial_idx, block_idx)
                lottery_data = lottery_trial.run_trial()
                all_data.append(lottery_data)

        # End-of-block trust rating for each partner
        for cpu_index, partner_config in enumerate(cpu_configs):
            block_end_trial = TrustGameTrial(
                UI_WIN=UI_WIN,
                PARAMETERS=PARAMETERS,
                partner_name=partner_config["name"],
                game_logic=game_logic,
                cpu_index=cpu_index,
                user_role="trustor",
                cpu_role="trustee",
                trialIdx=0,
                blockIdx=block_idx,
                partner_image=partner_images[partner_config["name"]]
            )
            end_block_ranking = block_end_trial.show_block_ranking()
            all_data.append({
                "blockIdx": block_idx,
                "partner": partner_config["name"],
                "end_block_ranking": end_block_ranking
            })

    # Mark the end of the experiment and save data
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
