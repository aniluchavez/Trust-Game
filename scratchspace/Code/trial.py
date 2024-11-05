import random
from os import path
from psychopy import core, event

import globals as glb
import stimuli as stim
from markEvent import markEvent


# conditional language generation
if glb.PARAMETERS.exp['language'] == 'English':
    import Text.EnglishTxt as txt
elif glb.PARAMETERS.exp['language'] == 'Spanish':
    import Text.SpanishTxt as txt

# FUNCTION THAT SHOWS THE WELCOME MESSAGE
def show_welcome():
    """" Welcome text. See EnglishTxt.py"""
    stim.draw_text(txt.SW_1, Pos=(0, 0), Height=40)
    glb.UI_WIN.flip()
    event.waitKeys(keyList=['return'])

    """"Let's begin!"""
    stim.draw_text(txt.SW_BEGIN, Height=50, Pos=(0, 0))
    glb.UI_WIN.flip()
    core.wait(3)


# FUNCTION TO PROMPT PARTICIPANT TO RATE PARTNER'S TRUSTWORTHINESS
def show_trust_ranking(PartnerImage:str, PartnerName:str, EventType:str, CpuIndex:int):
    stim.SLIDER.reset()
    response = -1
    responseTime = -1
    partnerImageName = path.join(glb.PARAMETERS.stimuli['imageFolder'], PartnerImage)
    markEvent(f'{EventType}Start', CpuIndex)
    glb.REL_CLOCK.reset()
    while response==-1:
        if glb.REL_CLOCK.getTime() < glb.PARAMETERS.timing['photodiode']:
            stim.PHOTODIODE.draw()
        stim.draw_image(partnerImageName, Pos=(0, 0.5), Size=(0.6, 0.8))
        """Partner: X"""
        stim.draw_text(f"{txt.STR_PARTNER}{PartnerName}", Height=50, Pos=(0, 0))
        """Please rate the trustworthiness of your partner on the scale below. Move slider with the arrow keys to desired ranking and press ENTER"""
        stim.draw_text(txt.STR_INSTR, Pos=(0, -0.3), Height=40)
        stim.SLIDER.draw()
        """Not Trustworthy"""
        stim.draw_text(txt.STR_UNTRUSTWORTHY, Pos=(-0.4, -0.6), Height=40)
        """Neutral"""
        stim.draw_text(txt.STR_NEUTRAL, Pos=(0, -0.6), Height=40)
        """Trustworthy"""
        stim.draw_text(txt.STR_TRUSTWORTHY, Pos=(0.4, -0.6), Height=40)
        glb.UI_WIN.flip()
        #added ability to move slider with arrows
        # Detecting arrow key input and moving the slider marker position
        keys = event.getKeys(keyList=['return', 'escape', 'left', 'right'])
        for key in keys:
            if key == 'return':
                responseTime = glb.REL_CLOCK.getTime()
                response = stim.SLIDER.getRating() or 5
            elif key == 'escape':
                glb.abort()
                response = -2
                markEvent("taskAbort")
            elif key == 'left':
                # Initialize markerPos to a default value if it's None
                if stim.SLIDER.markerPos is None:
                    stim.SLIDER.markerPos = stim.SLIDER.ticks[0]
                new_val = max(stim.SLIDER.markerPos - 1, stim.SLIDER.ticks[0])  # Ensures we stay within the min tick
                stim.SLIDER.markerPos = new_val
            elif key == 'right':
                # Initialize markerPos to a default value if it's None
                if stim.SLIDER.markerPos is None:
                    stim.SLIDER.markerPos = stim.SLIDER.ticks[0]
                new_val = min(stim.SLIDER.markerPos + 1, stim.SLIDER.ticks[-1])  # Ensures we stay within the max tick
                stim.SLIDER.markerPos = new_val

    if not glb.ABORT:
        # Respuesta registrada
        stim.draw_text(txt.STR_NOTED, Pos=(0, -0.9), Height=60)
        glb.UI_WIN.flip()

        markEvent(f'{EventType}End', CpuIndex)
        core.wait(1.5)

    return {'type': EventType,
            'partner': PartnerName,
            'ranking': response,
            'response_time': responseTime
            }


# FUNCTION FOR MAIN TRIAL SEQUENCE
def trust_trial(TrialIdx:int, BlockIdx:int, UserRole:str, CpuRole:str, GameLogic, CpuIndex:int, PartnerImage:str, PartnerName:str):
    GameLogic.set_fresh_pot()  # Set the fresh pot once per trial
    cpuResponse = "___"
    returnedAmount = -1
    markEvent("trialStart", TrialIdx, BlockIdx, 'trust')
    if UserRole == "trustor":
        userDecision = trust_decision_phase(GameLogic, CpuIndex, PartnerImage, PartnerName)
        if not glb.ABORT:
            cpuResponse, returnedAmount = trust_outcome_phase(userDecision, GameLogic, CpuIndex, PartnerName)
    else:
        cpuDecision = {"choice": "give", "amount": GameLogic.trustor_decision("give", CpuIndex)}
        cpuResponse, returnedAmount = trust_outcome_phase(cpuDecision, GameLogic, CpuIndex, PartnerName)
        userDecision = trust_decision_phase(GameLogic, CpuIndex, PartnerImage, PartnerName)
    
    if not glb.ABORT: markEvent("trialEnd", TrialIdx, BlockIdx, 'trust')
    return {
        "trial_type": f"Trust-{UserRole}",
        "response": userDecision['choice'],
        "partner": f'{PartnerName}-{CpuRole}',
        "outcome": cpuResponse,
        "response_time": userDecision['time'],
        "misc_info": f"${userDecision['fresh_pot']} -> ${returnedAmount}"
    }

# FUNCTION FOR QUICK TRANSITION FROM RANKING TO START OF THE TRIAL
def show_game_start_transition():
    """Starting the game. Get ready for the first trial..."""
    stim.draw_text(txt.SGST_TRANSITION, Pos=(0, 0), Height=50)
    glb.UI_WIN.flip()
    core.wait(2)  # Pauses for 3 seconds before starting the game

# FUNCTION TO PROCESS USER'S DECISION
def trust_decision_phase(GameLogic, CpuIndex:int, PartnerImage:str, PartnerName:str):
    # Initialize a fresh pot for this specific trial
    freshPot = GameLogic.current_fresh_pot  # Use the set fresh pot for this trial
    """ Keep $X"""
    keepButtonText = f"{txt.TDP_KEEP_BTN}{freshPot}"
    """Invest $X"""
    investButtonText = f"{txt.TDP_INVEST_BTN}{freshPot}"
    
    markEvent("DecisionStart")
    stim.PHOTODIODE.draw()
    trust_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText)
    core.wait(glb.PARAMETERS.timing['photodiode'])
    trust_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText)
    
    glb.REL_CLOCK.reset()
    keys = event.waitKeys(keyList=['f', 'j', 'escape'])
    responseTime = glb.REL_CLOCK.getTime()
    if 'escape' in keys:
        decision = 'keep'
        markEvent("taskAbort")
        glb.abort()
    elif 'f' in keys:
        decision = 'keep'
        highlight = 1
    elif 'j' in keys:
        decision = 'invest'
        highlight = 2

    if not glb.ABORT:
        stim.PHOTODIODE.draw()
        trust_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText, highlight)
        core.wait(glb.PARAMETERS.timing['photodiode'])
        trust_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText, highlight)
        core.wait(glb.PARAMETERS.timing['photodiode'])
        markEvent("DecisionEnd")

    amountInvolved = GameLogic.trustor_decision(decision, CpuIndex)

    return {"choice": decision, "amount": amountInvolved, 'time': responseTime, 'fresh_pot': freshPot}

def trust_decision_draw(PartnerName, PartnerImage, KeepButtonText, InvestButtonText, Highlight=None):
    keepLine = (255,255,255) if Highlight == 1 else (0, 0, 255)
    investLine = (255,255,255) if Highlight == 2 else (0, 0, 255)

    stim.draw_image(path.join(glb.PARAMETERS.stimuli['imageFolder'], PartnerImage), Pos=(0, 0.5), Size=(0.6, 0.8))
    """Partner: X"""
    stim.draw_text(f"{txt.TDD_PARTNER}{PartnerName}", Pos=(0, 0), Height=50)
    stim.draw_rect(FillColor=(0, 0, 255), LineColor=keepLine, Width=0.65, Height=0.2, Pos=(-0.4, -0.5))
    stim.draw_text(KeepButtonText, Pos=(-0.4, -0.5), Height=60)
    stim.draw_rect(FillColor=(0, 0, 255), LineColor=investLine, Width=0.65, Height=0.2, Pos=(0.4, -0.5))
    stim.draw_text(InvestButtonText, Pos=(0.4, -0.5), Height=60)
    """Press 'F' to Keep"""
    stim.draw_text(txt.TDD_KEEP_INSTR, Pos=(-0.4, -0.7), Height=54)
    """Press 'J' to Invest"""
    stim.draw_text(txt.TDD_INVEST_INSTR, Pos=(0.4, -0.7), Height=54)
    glb.UI_WIN.flip()

# FUNCTION TO PROCESS OUTCOME OF THE DECISION
def trust_outcome_phase(DecisionData:dict, GameLogic, CpuIndex:int, PartnerName:int):
    decision = DecisionData["choice"]
    amountGiven = DecisionData["amount"]

    markEvent("OutcomeStart")

    outcomeMessage = ...
    outcome = ...
    returnedAmount = ...
    if decision == "keep":
        """You kept $X"""
        outcomeMessage = f"{txt.TOP_KEPT}{amountGiven}"
        outcome = 'No Deal'
        returnedAmount = amountGiven
    else:
        returnedAmount = GameLogic.outcome_phase(amountGiven, CpuIndex)
        """X returned Y.     OR      X kept the money."""
        outcomeMessage = f"{PartnerName}{txt.TOP_RETURNED}{returnedAmount}" if returnedAmount > 0 else f"{PartnerName}{txt.TOP_STEAL}"
        outcome = 'Shared' if returnedAmount > 0 else 'Kept'
    stim.PHOTODIODE.draw()
    stim.draw_rect(FillColor=(0, 0, 255), Width=1, Height=0.4, Pos=(0, 0))
    stim.draw_text(outcomeMessage, Pos=(0, 0), Height=80)
    glb.UI_WIN.flip()
    core.wait(glb.PARAMETERS.timing['photodiode'])
    stim.draw_rect(FillColor=(0, 0, 255), Width=1, Height=0.4, Pos=(0, 0))
    stim.draw_text(outcomeMessage, Pos=(0, 0), Height=80)
    glb.UI_WIN.flip()

    markEvent("OutcomeEnd")

    core.wait(1.5)
    return outcome, returnedAmount


# FUNCTION FOR BLOCK TRANSITIONS and SUMMARIES
def show_cumulative_returns(CumulativeReturns, PartnerNames):
    """"End of Block Summary:\n\n"""
    returnText = txt.SCR_SUMMARY
    for cpu_index, total_returned in CumulativeReturns.items():
        partner_name = PartnerNames.get(cpu_index, f"Partner {cpu_index}")
        """ADD: X returned a total of $Y\n"""
        returnText += f"{partner_name}{txt.SCR_RETURN}{total_returned}\n"
    
    stim.draw_text(returnText, Pos=(0, 0), Height=70)
    glb.UI_WIN.flip()
    core.wait(4.5)  # Show summary for 4 seconds
 # Show summary for 4 seconds

def show_block_transition(BlockNumber):
    """End of Block X.\n\n Starting Block X+1...\n\nPress Enter to continue"""
    transitionText = f"{txt.SBT_1}{BlockNumber}{txt.SBT_2}{BlockNumber + 1}{txt.SBT_3}"
    stim.draw_text(transitionText, Pos=(0, 0), Height=55)
    glb.UI_WIN.flip()
    event.waitKeys(keyList=['return'], maxWait=20)

# FUNCTION USED TO SIMULATE A LOTTERY TRIAL
def lottery_trial(PartnerNames:str, TrialIdx, BlockIdx):
    suggestionPartner = random.choice(PartnerNames)
    """You decide whether or not to win the lottery"""
    suggestionText = txt.LT_SUGGESTION
    response = None
    investment_amount = random.randint(1, 5)
    """Invest $X for a chance to win 10x!"""
    lottery_info_text = f"{txt.LT_INFO_1}{investment_amount} {txt.LT_INFO_2}"

    markEvent("trialStart", TrialIdx, BlockIdx, 'lottery')
    markEvent("DecisionStart")

    stim.PHOTODIODE.draw()
    lot_decision_draw(lottery_info_text)   
    core.wait(glb.PARAMETERS.timing['photodiode'])
    lot_decision_draw(lottery_info_text)     
    glb.REL_CLOCK.reset()         

    keys = event.waitKeys(keyList=['f', 'j', 'escape'])
    responseTime = glb.REL_CLOCK.getTime()
    outcomeMessage = 'ABORT'
    outcome = 'ABORT'
    highlight=...
    if 'escape' in keys:
        response = "ABORT"
        glb.abort()
        markEvent('taskAbort')
    elif 'f' in keys:
        response = "yes"
        highlight = 1
        wonLottery = random.choice([True, False])  # 50% chance of winning
        outcome = "Won" if wonLottery else "Lost"
        """You won $X     OR    You lost the lottery"""
        outcomeMessage = f"{txt.LT_WON}{investment_amount * 10}!" if wonLottery else txt.LT_LOST
    elif 'j' in keys:
        highlight = 2
        response = "no"
        outcome = "Not Played"
        """You chose not to play the lottery"""
        outcomeMessage = txt.LT_QUIT
    
    if not glb.ABORT:
        stim.PHOTODIODE.draw()
        lot_decision_draw(lottery_info_text, highlight)   
        core.wait(glb.PARAMETERS.timing['photodiode'])
        lot_decision_draw(lottery_info_text, highlight)  
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

    return {"trial_type": "Lottery", "response": response, "partner": suggestionPartner, 
            "misc_info": suggestionText, "outcome": outcome, 'response_time': responseTime}

def lot_decision_draw(SuggestionText, Highlight=None):
    yesLine = (255,255,255) if Highlight == 1 else (0, 0, 255)
    noLine = (255,255,255) if Highlight == 2 else (0, 0, 255)

    stim.draw_image("Images/slot_machine.jpg", Pos=(0, 0.5), Size=(0.4, 0.8))
    stim.draw_text(SuggestionText, Pos=(0, -.05),Height=55, Color=(255,255,255))
    """Do you want to play the lottery?"""
    stim.draw_text(txt.LDD_QUESTION, Pos=(0,-0.3), Height=50)
    stim.draw_rect(FillColor=(0,0,255), LineColor=yesLine, Pos=(-0.3, -0.5), Width=0.3, Height=0.15)
    """Yes"""
    stim.draw_text(txt.LDD_YES, Pos=(-0.3, -0.5), Height=54)
    stim.draw_rect(FillColor=(0,0,255), LineColor=noLine, Pos=(0.3, -0.5), Width=0.3, Height=0.15)
    """No"""
    stim.draw_text(txt.LDD_NO, Pos=(0.3, -0.5), Height=54)
    """Press 'F' for Yes"""
    stim.draw_text(txt.LDD_YES_INSTR, Pos=(-0.3, -0.67), Height=43)
    """Press 'J' for No"""
    stim.draw_text(txt.LDD_NO_INSTR, Pos=(0.3, -0.67), Height=43)
    glb.UI_WIN.flip()           