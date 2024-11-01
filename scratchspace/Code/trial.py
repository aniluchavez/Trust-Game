import random
from os import path
from psychopy import core, event

import stimuli as stim
import globals as glb
from markEvent import markEvent


# FUNCTION THAT SHOWS THE WELCOME MESSAGE
def show_welcome1():
    """Display welcome message and game instructions at the start of the experiment."""
    welcomeText = "Welcome to the Trust Game Experiment!\n\nIn this game, you'll be interacting with a partner that prerecorded their responses.\n\n" +\
                  "You are the trustor.\n"+\
                  "You can choose to keep or invest money, and your partner may choose to share up to 3X your initial investment or keep it all for themselves.\n\n"+\
                  "Press 'Enter' to continue."
    stim.draw_text(welcomeText, Pos=(0, 0), Height=40)
    glb.UI_WIN.flip()
    event.waitKeys(keyList=['return'], maxWait=20)
    stim.draw_text("Let's begin!", Height=50, Pos=(0, 0))
    glb.UI_WIN.flip()
    core.wait(3)


# FUNCTION TO PROMPT PARTICIPANT TO RATE PARTNER'S TRUSTWORTHINESS
INSTRUCTIONS_TEXT = "Please rate the trustworthiness of your partner on the scale below. Move slider with trackpad to desired ranking and press ENTER"
def show_trust_ranking(PartnerImage:str, PartnerName:str, EventType:str, CpuIndex:int):
    stim.SLIDER.reset()
    response = None
    partnerImageName = path.join(glb.PARAMETERS.stimuli['imageFolder'], PartnerImage)
    markEvent(f'{EventType}Start', CpuIndex)
    glb.REL_CLOCK.reset()
    while response is None:
        if glb.REL_CLOCK.getTime() < glb.PARAMETERS.timing['photodiode']:
            stim.PHOTODIODE.draw()
        stim.draw_image(partnerImageName, Pos=(0, 0.5), Size=(0.6, 0.8))
        stim.draw_text(f"Partner: {PartnerName}", Height=50, Pos=(0, 0))
        stim.draw_text(INSTRUCTIONS_TEXT, Pos=(0, -0.3), Height=40)
        stim.SLIDER.draw()
        stim.draw_text("Not Trustworthy", Pos=(-0.4, -0.6), Height=40)
        stim.draw_text("Neutral", Pos=(0, -0.6), Height=40)
        stim.draw_text("Trustworthy", Pos=(0.4, -0.6), Height=40)
        glb.UI_WIN.flip()
        keys = event.getKeys(keyList=['return'])
        if 'return' in keys:
            response = stim.SLIDER.getRating() or 5
            markEvent(EventType, rating=response, time=glb.ABS_CLOCK.getTime())
    stim.draw_text("Response noted.", Pos=(0, -0.9), Height=60)
    glb.UI_WIN.flip()

    markEvent(f'{EventType}End', CpuIndex)
    core.wait(3)
    return response


# FUNCTION FOR MAIN TRIAL SEQUENCE
def normal_trial(TrialIdx:int, BlockIdx:int, UserRole:str, CpuRole:str, GameLogic, CpuIndex:int, PartnerImage:str, PartnerName:str):
    glb.reset_clock()
    GameLogic.set_fresh_pot()  # Set the fresh pot once per trial
    
    markEvent("trialStart", TrialIdx, BlockIdx, 'trust')
    if UserRole == "trustor":
        userDecision = normal_decision_phase(GameLogic, CpuIndex, PartnerImage, PartnerName)
        decision_time = glb.ABS_CLOCK.getTime()
        # markEvent("UserChoice", role=UserRole, decision=userDecision["choice"], time=decision_time)
        cpu_response = normal_outcome_phase(userDecision, GameLogic, CpuIndex, PartnerName)
        outcome_time = glb.ABS_CLOCK.getTime()
        # markEvent("OutcomeEnd", returned_amount=cpu_response["amount_returned"], time=outcome_time)
    else:
        cpuDecision = {"choice": "give", "amount": GameLogic.trustor_decision("give", CpuIndex)}
        cpu_response = normal_outcome_phase(cpuDecision, GameLogic, CpuIndex, PartnerName)
        userDecision = normal_decision_phase(GameLogic, CpuIndex, PartnerImage, PartnerName)
        # markEvent("UserChoice", role=UserRole, decision=userDecision["choice"])
    
    markEvent("trialEnd", TrialIdx, BlockIdx, 'trust')
    return {
        "trialIdx": TrialIdx,
        "blockIdx": BlockIdx,
        "user_role": UserRole,
        "cpu_role": CpuRole,
        "user_decision": userDecision,
        "cpu_response": cpu_response,
    }



# FUNCTION TO PROCESS USER'S DECISION
def normal_decision_phase(GameLogic, CpuIndex:int, PartnerImage:str, PartnerName:str):
    # Initialize a fresh pot for this specific trial
    fresh_pot = GameLogic.current_fresh_pot  # Use the set fresh pot for this trial
    
    keepButtonText = f"Keep ${fresh_pot}"
    investButtonText = f"Invest ${fresh_pot}"
    
    markEvent("DecisionStart")
    stim.PHOTODIODE.draw()
    norm_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText)
    core.wait(glb.PARAMETERS.timing['photodiode'])
    norm_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText)

    keys = event.waitKeys(keyList=['f', 'j', 'escape'])
    if 'escape' in keys:
        core.quit()
    decision = 'keep' if 'f' in keys else 'invest'
    highlight = 1 if 'f' in keys else 2

    stim.PHOTODIODE.draw()
    norm_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText, highlight)
    core.wait(glb.PARAMETERS.timing['photodiode'])
    norm_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText, highlight)
    core.wait(glb.PARAMETERS.timing['photodiode'])

    amount_involved = GameLogic.trustor_decision(decision, CpuIndex)

    markEvent("DecisionEnd")
    return {"choice": decision, "amount": amount_involved}

def norm_decision_draw(PartnerName, PartnerImage, KeepButtonText, InvestButtonText, Highlight=None):
    keepLine = (255,255,255) if Highlight == 1 else (0, 0, 255)
    investLine = (255,255,255) if Highlight == 2 else (0, 0, 255)

    stim.draw_image(path.join(glb.PARAMETERS.stimuli['imageFolder'], PartnerImage), Pos=(0, 0.5), Size=(0.6, 0.8))
    stim.draw_text(f"Partner: {PartnerName}", Pos=(0, 0), Height=50)
    stim.draw_rect(FillColor=(0, 0, 255), LineColor=keepLine, Width=0.6, Height=0.2, Pos=(-0.4, -0.5))
    stim.draw_text(KeepButtonText, Pos=(-0.4, -0.5), Height=60)
    stim.draw_rect(FillColor=(0, 0, 255), LineColor=investLine, Width=0.6, Height=0.2, Pos=(0.4, -0.5))
    stim.draw_text(InvestButtonText, Pos=(0.4, -0.5), Height=60)
    stim.draw_text("Press 'F' to Keep", Pos=(-0.4, -0.7), Height=54)
    stim.draw_text("Press 'J' to Invest", Pos=(0.4, -0.7), Height=54)
    glb.UI_WIN.flip()

# FUNCTION TO PROCESS OUTCOME OF THE DECISION
def normal_outcome_phase(DecisionData:dict, GameLogic, CpuIndex:int, PartnerName:int):
    decision = DecisionData["choice"]
    amountGiven = DecisionData["amount"]

    markEvent("OutcomeStart")

    if decision == "keep":
        outcomeMessage = f"You kept ${amountGiven}"
        returned_amount = 0
    else:
        returned_amount = GameLogic.outcome_phase(amountGiven, CpuIndex)
        outcomeMessage = f"{PartnerName} returned ${returned_amount}" if returned_amount > 0 else f"{PartnerName} kept the money"
        #if GameLogic.trustor_balances[CpuIndex] == GameLogic.initial_money:
        #    outcomeMessage += f" (Your balance was replenished to ${GameLogic.initial_money})" #may need to remove this, no need for rep

    stim.PHOTODIODE.draw()
    stim.draw_rect(FillColor=(0, 0, 255), Width=0.99, Height=0.4, Pos=(0, 0))
    stim.draw_text(outcomeMessage, Pos=(0, 0), Height=80)
    glb.UI_WIN.flip()
    core.wait(glb.PARAMETERS.timing['photodiode'])
    stim.draw_rect(FillColor=(0, 0, 255), Width=0.99, Height=0.4, Pos=(0, 0))
    stim.draw_text(outcomeMessage, Pos=(0, 0), Height=80)
    glb.UI_WIN.flip()

    markEvent("OutcomeEnd")

    core.wait(2)
    return {
        "choice": decision,
        "amount_given": amountGiven if decision == "invest" else 0,
        "amount_returned": returned_amount if decision == "invest" else 0
    }


# FUNCTION USED TO SIMULATE A LOTTERY TRIAL
def lottery_trial(PartnerNames:str, TrialIdx, BlockIdx):
    suggestionType = "partner" if random.random() < 0.5 else "self"
    suggestionText = f"{random.choice(PartnerNames)} suggests you {'enter' if random.random() < 0.5 else 'do not enter'} the lottery." \
                     if suggestionType == "partner" else "You decide whether to enter the lottery."

    response = None
    markEvent("trialStart", TrialIdx, BlockIdx, 'lottery')
    markEvent("DecisionStart")

    stim.PHOTODIODE.draw()
    lot_decision_draw(suggestionText)   
    core.wait(glb.PARAMETERS.timing['photodiode'])
    lot_decision_draw(suggestionText)              

    keys = event.waitKeys(keyList=['f', 'j', 'escape'])
    outcomeMessage = 'ABORT'
    highlight=...
    if 'escape' in keys:
        core.quit()
    elif 'f' in keys:
        response = "yes"
        highlight = 1
        wonLottery = random.randint(0, 1) == 1
        outcomeMessage = "You won the lottery!" if wonLottery else "You did not win the lottery."
    elif 'j' in keys:
        highlight = 2
        response = "no"
        outcomeMessage = "You chose not to play the lottery."
    
    stim.PHOTODIODE.draw()
    lot_decision_draw(suggestionText, highlight)   
    core.wait(glb.PARAMETERS.timing['photodiode'])
    lot_decision_draw(suggestionText, highlight)  
    core.wait(glb.PARAMETERS.timing['photodiode'])

    markEvent("DecisionEnd")
    markEvent("OutcomeStart")

    stim.PHOTODIODE.draw()
    stim.draw_rect(FillColor=(0,0,255), Width=0.9, Height=0.4, Pos=(0,0))
    stim.draw_text(outcomeMessage, Height=54)
    glb.UI_WIN.flip()
    core.wait(glb.PARAMETERS.timing['photodiode'])
    stim.draw_rect(FillColor=(0,0,255), Width=0.9, Height=0.4, Pos=(0,0))
    stim.draw_text(outcomeMessage, Height=54)
    glb.UI_WIN.flip()

    markEvent("OutcomeEnd")
    markEvent("trialEnd", TrialIdx, BlockIdx, 'lottery')

    core.wait(2)

    return {"trial_type": "lottery", "response": response, "suggestion_text": suggestionText}

def lot_decision_draw(SuggestionText, Highlight=None):
    yesLine = (255,255,255) if Highlight == 1 else (0, 0, 255)
    noLine = (255,255,255) if Highlight == 2 else (0, 0, 255)

    stim.draw_image("Images/slot_machine.jpg", Pos=(0, 0.5), Size=(0.4, 0.8))
    stim.draw_text(SuggestionText, Pos=(0, -.05),Height=55, Color=(255,255,255))
    stim.draw_text("Do you want to play the lottery?", Pos=(0,-0.3), Height=50)
    stim.draw_rect(FillColor=(0,0,255), LineColor=yesLine, Pos=(-0.3, -0.5), Width=0.3, Height=0.15)
    stim.draw_text("Yes", Pos=(-0.3, -0.5), Height=54)
    stim.draw_rect(FillColor=(0,0,255), LineColor=noLine, Pos=(0.3, -0.5), Width=0.3, Height=0.15)
    stim.draw_text("No", Pos=(0.3, -0.5), Height=54)
    stim.draw_text("Press F for Yes", Pos=(-0.3, -0.67), Height=43)
    stim.draw_text("Press J for No", Pos=(0.3, -0.67), Height=43)
    glb.UI_WIN.flip()           