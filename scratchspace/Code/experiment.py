import random
from psychopy import core
import globals as glb
import trial
from markEvent import markEvent
from Class.game_logic import GameLogic

def run_experiment():
    allData = []
    trial.show_welcome()
    
    numBlocks, numTrialsPerBlock = glb.PARAMETERS.get_block_info()
    partnerImages = {}  # Store preloaded images to avoid reloading

    for blockIdx in range(numBlocks):
        cpuConfigs = glb.PARAMETERS.get_block_partners(blockIdx)
        
        # Initialize `GameLogic` once and update configuration each block if needed
        if blockIdx == 0:
            gameLogic = GameLogic(cpuConfigs, initial_money=1)
        else:
            gameLogic.update_partners(cpuConfigs)  # Hypothetical update function

        for partner in cpuConfigs:
            if partner["name"] not in partnerImages:
                partnerImages[partner["name"]] = partner["image"]  # Load once

        allInitialRatings = {}
        for cpuIndex, partnerConfig in enumerate(cpuConfigs):
            if partnerConfig["name"] not in allInitialRatings:
                initialRating = trial.show_trust_ranking(partnerImages[partnerConfig["name"]], partnerConfig["name"], "IntroSlider")
                allInitialRatings[partnerConfig["name"]] = initialRating
                allData.append({"blockIdx": blockIdx, "partner": partnerConfig["name"], "initial_rating": initialRating})

        interleaved_trials = glb.PARAMETERS.get_interleaved_trial_types(numTrialsPerBlock)

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

        for cpuIndex, partnerConfig in enumerate(cpuConfigs):
            endBlockRanking = trial.show_trust_ranking(partnerImages[partnerConfig["name"]], partnerConfig["name"], "BlockEndRanking")
            allData.append({"blockIdx": blockIdx, "partner": partnerConfig["name"], "end_block_ranking": endBlockRanking})

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
