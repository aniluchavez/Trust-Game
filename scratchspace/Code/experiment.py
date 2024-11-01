import random
from psychopy import core
import globals as glb
import trial
from markEvent import markEvent
from Class.game_logic import GameLogic

def run_experiment():
    allData = []

    # Show welcome screen
    trial.show_welcome1()
    
    # Experiment structure from parameters
    numBlocks, numTrialsPerBlock = glb.PARAMETERS.get_block_info()
    partners = glb.PARAMETERS.get_block_partners(0)  # Retrieve the consistent partners list
    gameLogic = GameLogic(partners)  # Initialize GameLogic once for consistent partners

    # Generate partner images only once, as partners are the same across blocks
    partnerImages = {partner['name']: partner['image'] for partner in partners}

    # Loop through each block
    for blockIdx in range(numBlocks):
        # Collect ratings at the start of Block 1, Block 5, and the end of Block 10
        if blockIdx == 0 or blockIdx == 4:  # Start of Block 1 or Block 5
            for cpuIndex, partnerConfig in enumerate(partners):
                initialRating = trial.show_trust_ranking(partnerImages[partnerConfig["name"]], partnerConfig["name"], "TrustRankInitial", cpuIndex)
                allData.append({
                    "blockIdx": blockIdx,
                    "partner": partnerConfig["name"],
                    "rating": initialRating,
                    "rating_type": "initial" if blockIdx == 0 else "midpoint"
                })

        # Generate the trial types for the current block
        interleaved_trials = glb.PARAMETERS.get_interleaved_trial_types(numTrialsPerBlock, blockIdx)
        print(f"Block {blockIdx + 1} trial types:", interleaved_trials)  # Debug statement

        # Run each trial based on the interleaved structure
        for trialIdx, trialType in enumerate(interleaved_trials):
            if trialType == "trust":
                cpuIndex, partnerConfig = random.choice(list(enumerate(partners)))
                trialData = trial.normal_trial(trialIdx, blockIdx, "trustor", "trustee", gameLogic, cpuIndex, 
                                               partnerImages[partnerConfig["name"]], partnerConfig["name"])
                trialData["blockIdx"] = blockIdx
                allData.append(trialData)

            elif trialType == "lottery":
                lotteryData = trial.lottery_trial(list(partnerImages.keys()),trialIdx,blockIdx)
                lotteryData["blockIdx"] = blockIdx
                allData.append(lotteryData)

    # Collect final ratings at the end of Block 10
    if blockIdx == 9:  # End of Block 10
        for cpuIndex, partnerConfig in enumerate(partners):
            finalRating = trial.show_trust_ranking(partnerImages[partnerConfig["name"]], partnerConfig["name"], "TrustRankFinal", cpuIndex)
            allData.append({
                "blockIdx": blockIdx,
                "partner": partnerConfig["name"],
                "rating": finalRating,
                "rating_type": "final"
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
