import random, math
import globals as glb
import pandas as pd

import trial
from markEvent import markEvent
from Class.game_logic import GameLogic

def run_experiment():
    allTrials = []
    allRankings = []
    midBlock = math.floor( (glb.PARAMETERS.exp['numBlocks']-1)/2 )

    # Show welcome screen
    trial.show_welcome()
    
    # Experiment structure from parameters
    numBlocks, numTrialsPerBlock = glb.PARAMETERS.get_block_info()
    partners = glb.PARAMETERS.get_block_partners(0)  # Retrieve the consistent partners list
    gameLogic = GameLogic(partners)  # Initialize GameLogic once for consistent partners

    # Generate partner images only once, as partners are the same across blocks
    partnerImages = {partner['name']: partner['image'] for partner in partners}

    # Loop through each block
    for blockIdx in range(numBlocks):
        blockTrials = []
        blockRankings = []
        # Collect ratings at the start of Block 1, Block 5, and the end of Block 10
        if blockIdx == 0 or blockIdx == midBlock:  # Start of Block 1 or Block 5
            for cpuIndex, partnerConfig in enumerate(partners):
                if glb.ABORT: 
                    break
                eventType = "TrustRankInitial" if blockIdx == 0 else "TrustRankMiddle"
                initialRating = trial.show_trust_ranking(partnerImages[partnerConfig["name"]], partnerConfig["name"], eventType, cpuIndex)
                formatedData = format_data('Ranking', initialRating)
                blockRankings.append(formatedData)
                allRankings.append(formatedData)

        if not glb.ABORT:
            # Generate the trial types for the current block
            interleaved_trials = glb.PARAMETERS.get_interleaved_trial_types(numTrialsPerBlock, blockIdx)
            print(f"Block {blockIdx + 1} trial types:", interleaved_trials)  # Debug statement

            # Run each trial based on the interleaved structure
            for trialIdx, trialType in enumerate(interleaved_trials):
                trialData = ...
                if trialType == "trust":
                    cpuIndex, partnerConfig = random.choice(list(enumerate(partners)))
                    trialData = trial.normal_trial(trialIdx, blockIdx, "trustor", "trustee", gameLogic, cpuIndex, 
                                                   partnerImages[partnerConfig["name"]], partnerConfig["name"])

                elif trialType == "lottery":
                    trialData = trial.lottery_trial(list(partnerImages.keys()),trialIdx,blockIdx)

                trialData["blockIdx"] = blockIdx+1
                formatedData = format_data('Trial', trialData)
                blockTrials.append(formatedData)
                allTrials.append(formatedData)

                if glb.ABORT: break

        if not glb.ABORT:
            # Collect final ratings at the end of Block 10
            if blockIdx == 9:  # End of Block 10
                for cpuIndex, partnerConfig in enumerate(partners):
                    finalRating = trial.show_trust_ranking(partnerImages[partnerConfig["name"]], partnerConfig["name"], "TrustRankFinal", cpuIndex)
                    formatedData = format_data('Ranking', finalRating)
                    blockRankings.append(formatedData)
                    allRankings.append(formatedData)

        blockTrialsDataFrame = pd.DataFrame(blockTrials, columns=["Trial Type", "Block", "User Response", "Partner Name", "Trial Outcome", "Response Time", "Misc"])
        blockTrialsDataFrame.to_excel(glb.PARAMETERS.outputDir+f'BlockTrials_{blockIdx+1}.xlsx')
        
        if len(blockRankings) > 0:
            blockRankingsDataFrame = pd.DataFrame(blockRankings, columns=["Ranking Type", "Partner Name", "User Ranking", "Response Time"])
            blockRankingsDataFrame.to_excel(glb.PARAMETERS.outputDir+f'BlockRankings_{blockIdx+1}.xlsx')
        
        if glb.ABORT: break

    # Mark the end of the experiment and save data
    if not glb.ABORT: markEvent("taskStop", PARAMETERS=glb.PARAMETERS)
    
    trialsDataFrame = pd.DataFrame(blockTrials, columns=["Trial Type", "Block", "User Response", "Partner Name", "Trial Outcome", "Response Time", "Misc"])
    trialsDataFrame.to_excel(glb.PARAMETERS.outputDir+f'AllTrials.xlsx')

    rankingsDataFrame = pd.DataFrame(blockRankings, columns=["Ranking Type", "Partner Name", "User Ranking", "Response Time"])
    rankingsDataFrame.to_excel(glb.PARAMETERS.outputDir+f'AllRankings.xlsx')

    eventDataFrame = pd.DataFrame(glb.EVENTS, columns=["Event Name", "Event Time"])
    eventDataFrame.to_excel(glb.PARAMETERS.outputDir+f'Event Data.xlsx')

    # save_data(allData)
    glb.UI_WIN.close()



def format_data(Format, Data):
    match Format:
        case 'Trial':
            return (str(Data['trial_type']), int(Data['blockIdx']), str(Data['response']), str(Data['partner']), 
                    str(Data['outcome']), float(Data['response_time']), str(Data['misc_info']))
        case 'Ranking':
            return (str(Data['type']), str(Data['partner']), int(Data['ranking']), float(Data['response_time']))
# def save_data(data_records, filename="experiment_data"):
#     import csv, os
#     filepath = os.path.join(glb.DATA_PATH, f"{filename}.csv")
#     with open(filepath, 'w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=data_records[0].keys())
#         writer.writeheader()
#         writer.writerows(data_records)
