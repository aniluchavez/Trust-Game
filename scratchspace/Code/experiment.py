import random

from psychopy import core

import globals as glb
import trial
from markEvent import markEvent

from Class.game_logic import GameLogic

def run_experiment():
    allData = []

    # Show welcome screen
    trial.show_welcome()
    
    # Experiment structure from parameters
    numBlocks, numTrialsPerBlock = glb.PARAMETERS.get_block_info()

    # Loop through each block
    for blockIdx in range(numBlocks):
        cpuConfigs = glb.PARAMETERS.get_block_partners(blockIdx)

        # Initialize GameLogic with selected partners for each block
        gameLogic = GameLogic(cpuConfigs, initial_money=1)
        gameLogic.reset_amounts()

        # Generate all of the partner images
        partnerImages={partner['name']: partner['image'] for partner in cpuConfigs}

        # Show initial trust rating for each partner only once per block
        allInitialRatings = {}
        for cpuIndex, partnerConfig in enumerate(cpuConfigs):
            if partnerConfig["name"] not in allInitialRatings:
                initialRating = trial.show_trust_ranking(partnerImages[partnerConfig["name"]], partnerConfig["name"], "IntroSlider")
                allInitialRatings.update({partnerConfig["name"]: initialRating})
                allData.append({
                    "blockIdx": blockIdx,
                    "partner": partnerConfig["name"],
                    "initial_rating": initialRating
                })

        # Generate interleaved trial list using get_interleaved_trial_types only
        interleaved_trials = glb.PARAMETERS.get_interleaved_trial_types(numTrialsPerBlock)
        print(f"Block {blockIdx + 1} trial types:", interleaved_trials)  # Debug statement

        # Run each trial based on the interleaved structure
        for trialIdx, trialType in enumerate(interleaved_trials):
            if trialType == "trust":
                cpuIndex, partnerConfig = random.choice(list(enumerate(cpuConfigs)))
                trialData = trial.normal_trial(trialIdx, blockIdx, "trustor", "trustee", gameLogic, cpuIndex, 
                                               partnerImages[partnerConfig["name"]], partnerConfig["name"])
                trialData["initial_rating"] = allInitialRatings[partnerConfig["name"]]
                allData.append(trialData)

            elif trialType == "lottery":
                lotteryData = trial.lottery_trial(list(partnerImages.keys()))
                allData.append(lotteryData)

        # End-of-block trust rating for each partner
        for cpuIndex, partnerConfig in enumerate(cpuConfigs):
            endBlockRanking = trial.show_trust_ranking(partnerImages[partnerConfig["name"]], partnerConfig["name"], "BlockEndRanking")
            allData.append({
                "blockIdx": blockIdx,
                "partner": partnerConfig["name"],
                "end_block_ranking": endBlockRanking
            })

    # Mark the end of the experiment and save data
    markEvent("taskStop", PARAMETERS=glb.PARAMETERS)
    save_data(allData)
    glb.UI_WIN.close()

def save_data(data_records, filename="experiment_data"):
    import csv, os
    filepath = os.path.join(glb.DATA_PATH, f"{filename}.csv")
    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data_records[0].keys())
        writer.writeheader()
        writer.writerows(data_records)
