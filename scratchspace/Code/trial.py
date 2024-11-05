import random
from os import path
from psychopy import core, event

import globals as glb
import stimuli as stim
from markEvent import markEvent


# conditional language generation
if glb.PARAMETERS.exp['language'] == 'English':
    import Text.EnglishTxt as txt

# FUNCTION THAT SHOWS THE WELCOME MESSAGE
def show_welcome():
    """Display welcome message and game instructions at the start of the experiment."""
    # Bienvenido al experimento del Juego de la Confianza. En este juego tu estaras interactuando con un companero que previamente a selecionado previamente sus respuestas.
    # Puedes escoger entre invertir o quedarte con tu dinero
    # Y tu companero puede decidir entre regresar hasta tres veces tu inversion o quedarselo
    # Presione 'ENTER' para continuar
    # Eligiendo a tus companeros ...
    # Vamos a empezar
    # welcomeText = "Welcome to the Trust Game Experiment!\n\nIn this game, you'll be interacting with a partner that prerecorded their responses.\n\n" +\
    #               "You are the trustor.\n"+\
    #               "You can choose to keep or invest money, and your partner may choose to share up to 3X your initial investment or keep it all for themselves.\n\n"+\
    #               "Press 'Enter' to continue."
    # stim.draw_text(welcomeText, Pos=(0, 0), Height=40)
    """" Welcome text. See EnglishTxt.py"""
    stim.draw_text(txt.SW_1, Pos=(0, 0), Height=40)
    glb.UI_WIN.flip()
    event.waitKeys(keyList=['return'], maxWait=20)
    # stim.draw_text("Let's begin!", Height=50, Pos=(0, 0))

    """"Let's begin!"""
    stim.draw_text(txt.SW_BEGIN, Height=50, Pos=(0, 0))
    glb.UI_WIN.flip()
    core.wait(3)


# FUNCTION TO PROMPT PARTICIPANT TO RATE PARTNER'S TRUSTWORTHINESS
#Spanish instructions: Por favor califica la confianza que le tienes a esta persona usando la escala inferior. Mueve las flechas del teclado <>
# para elegir tu grado de confianza y presiona 'ENTER'
# INSTRUCTIONS_TEXT = "Please rate the trustworthiness of your partner on the scale below. Move slider with the arrow keys to desired ranking and press ENTER"
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
        # stim.draw_text(f"Partner: {PartnerName}", Height=50, Pos=(0, 0))
        # stim.draw_text(INSTRUCTIONS_TEXT, Pos=(0, -0.3), Height=40)
        stim.SLIDER.draw()
        # no confiable, neutral, confianble
        """Not Trustworthy"""
        stim.draw_text(txt.STR_UNTRUSTWORTHY, Pos=(-0.4, -0.6), Height=40)
        """Neutral"""
        stim.draw_text(txt.STR_NEUTRAL, Pos=(0, -0.6), Height=40)
        """Trustworthy"""
        stim.draw_text(txt.STR_TRUSTWORTHY, Pos=(0.4, -0.6), Height=40)
        # stim.draw_text("Not Trustworthy", Pos=(-0.4, -0.6), Height=40)
        # stim.draw_text("Neutral", Pos=(0, -0.6), Height=40)
        # stim.draw_text("Trustworthy", Pos=(0.4, -0.6), Height=40)
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
        # stim.draw_text("Response noted.", Pos=(0, -0.9), Height=60)
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
    # transition_text = "Starting the game. Get ready for the first trial..."
    """Starting the game. Get ready for the first trial..."""
    stim.draw_text(txt.SGST_TRANSITION, Pos=(0, 0), Height=50)
    # stim.draw_text(transition_text, Pos=(0, 0), Height=50)
    glb.UI_WIN.flip()
    core.wait(2)  # Pauses for 3 seconds before starting the game

# FUNCTION TO PROCESS USER'S DECISION
def trust_decision_phase(GameLogic, CpuIndex:int, PartnerImage:str, PartnerName:str):
    # Initialize a fresh pot for this specific trial
    freshPot = GameLogic.current_fresh_pot  # Use the set fresh pot for this trial
    # Guardar , Invertir 
    """ Keep $X"""
    keepButtonText = f"{txt.TDP_KEEP_BTN}{freshPot}"
    """Invest $X"""
    investButtonText = f"{txt.TDP_INVEST_BTN}{freshPot}"
    # keepButtonText = f"Keep ${freshPot}"
    # investButtonText = f"Invest ${freshPot}"
    
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
    # stim.draw_text(f"Partner: {PartnerName}", Pos=(0, 0), Height=50)\
    """Partner: X"""
    stim.draw_text(f"{txt.TDD_PARTNER}{PartnerName}", Pos=(0, 0), Height=50)
    stim.draw_rect(FillColor=(0, 0, 255), LineColor=keepLine, Width=0.6, Height=0.2, Pos=(-0.4, -0.5))
    stim.draw_text(KeepButtonText, Pos=(-0.4, -0.5), Height=60)
    stim.draw_rect(FillColor=(0, 0, 255), LineColor=investLine, Width=0.6, Height=0.2, Pos=(0.4, -0.5))
    stim.draw_text(InvestButtonText, Pos=(0.4, -0.5), Height=60)
    """Press 'F' to Keep"""
    stim.draw_text(txt.TDD_KEEP_INSTR, Pos=(-0.4, -0.7), Height=54)
    """Press 'J' to Invest"""
    stim.draw_text(txt.TDD_INVEST_INSTR, Pos=(0.4, -0.7), Height=54)
    # stim.draw_text("Press 'F' to Keep", Pos=(-0.4, -0.7), Height=54)
    # stim.draw_text("Press 'J' to Invest", Pos=(0.4, -0.7), Height=54)
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
        # Tu guardaste  
        # outcomeMessage = f"You kept ${amountGiven}"
        """You kept $X"""
        outcomeMessage = f"{txt.TOP_KEPT}{amountGiven}"
        outcome = 'No Deal'
        returnedAmount = amountGiven
    else:
        #  X regreso , X se quedo con el dinero
        returnedAmount = GameLogic.outcome_phase(amountGiven, CpuIndex)
        # outcomeMessage = f"{PartnerName} returned ${returnedAmount}" if returnedAmount > 0 else f"{PartnerName} kept the money"
        """X returned Y.     OR      X kept the money."""
        outcomeMessage = f"{PartnerName}{txt.TOP_RETURNED}{returnedAmount}" if returnedAmount > 0 else f"{PartnerName}{txt.TOP_STEAL}"
        outcome = 'Shared' if returnedAmount > 0 else 'Kept'
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
    return outcome, returnedAmount


# FUNCTION FOR BLOCK TRANSITIONS and SUMMARIES
def show_cumulative_returns(CumulativeReturns, PartnerNames):
    # return_text = "End of Block Summary:\n\n"
    """"End of Block Summary:\n\n"""
    returnText = txt.SCR_SUMMARY
    for cpu_index, total_returned in CumulativeReturns.items():
        partner_name = PartnerNames.get(cpu_index, f"Partner {cpu_index}")
        # return_text += f"{partner_name} returned a total of ${total_returned}\n"
        """ADD: X returned a total of $Y\n"""
        returnText += f"{partner_name}{txt.SCR_RETURN}{total_returned}\n"
    
    stim.draw_text(returnText, Pos=(0, 0), Height=70)
    glb.UI_WIN.flip()
    core.wait(4)  # Show summary for 4 seconds
 # Show summary for 4 seconds

def show_block_transition(BlockNumber):
    """Display end of block message and indicate the start of the next block."""
    # transition_text = f"End of Block {BlockNumber}\n\nStarting Block {BlockNumber + 1}...\n\nPress 'Enter' to continue."
    """End of Block X.\n\n Starting Block X+1...\n\nPress Enter to continue"""
    transitionText = f"{txt.SBT_1}{BlockNumber}{txt.SBT_2}{BlockNumber + 1}{txt.SBT_3}"
    stim.draw_text(transitionText, Pos=(0, 0), Height=55)
    glb.UI_WIN.flip()
    event.waitKeys(keyList=['return'], maxWait=20)

# FUNCTION USED TO SIMULATE A LOTTERY TRIAL
def lottery_trial(PartnerNames:str, TrialIdx, BlockIdx):
    suggestionType = "partner" if random.random() < 0.5 else "self"
    suggestionPartner = random.choice(PartnerNames)
    # sugiere que entres a a loteria, sugiere que no entres a lo loteria, tu decide si quieres entrar a la loteria
    # suggestionText = "You decide whether to enter the lottery."
    """You decide whether or not to win the lottery"""
    suggestionText = txt.LT_SUGGESTION
    # f"{suggestionPartner} suggests you {'enter' if random.random() < 0.5 else 'do not enter'} the lottery." \
    #                      if suggestionType == "partner" else 
    response = None
    investment_amount = random.randint(1, 5)
    # lottery_info_text = f"Invest ${investment_amount} with a chance to multiply by 10!"
    lottery_info_text = f"{txt.LT_INFO_1}{investment_amount}. {txt.LT_INFO_2}"

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
        # Ganaste , No ganaste la loteria
        # outcomeMessage = f"You won ${investment_amount * 10}!" if wonLottery else "You did not win the lottery."
        """You won $X     OR    You lost the lottery"""
        outcomeMessage = f"{txt.LT_WON}{investment_amount * 10}!" if wonLottery else txt.LT_LOST
    elif 'j' in keys:
        highlight = 2
        response = "no"
        outcome = "Not Played"
        # Decidiste no entrar a la loteria
        # outcomeMessage = "You chose not to play the lottery."
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
    # Quieres jugar a la loteria ? 
    # stim.draw_text("Do you want to play the lottery?", Pos=(0,-0.3), Height=50)
    stim.draw_text(txt.LDD_QUESTION, Pos=(0,-0.3), Height=50)
    stim.draw_rect(FillColor=(0,0,255), LineColor=yesLine, Pos=(-0.3, -0.5), Width=0.3, Height=0.15)
    # stim.draw_text("Yes", Pos=(-0.3, -0.5), Height=54)
    stim.draw_text(txt.LDD_YES, Pos=(-0.3, -0.5), Height=54)
    stim.draw_rect(FillColor=(0,0,255), LineColor=noLine, Pos=(0.3, -0.5), Width=0.3, Height=0.15)
    # stim.draw_text("No", Pos=(0.3, -0.5), Height=54)
    stim.draw_text(txt.LDD_NO, Pos=(0.3, -0.5), Height=54)
    #Presiona F para Si, Presiona J para No
    stim.draw_text(txt.LDD_YES_INSTR, Pos=(-0.3, -0.67), Height=43)
    stim.draw_text(txt.LDD_NO_INSTR, Pos=(0.3, -0.67), Height=43)
    # stim.draw_text("Press F for Yes", Pos=(-0.3, -0.67), Height=43)
    # stim.draw_text("Press J for No", Pos=(0.3, -0.67), Height=43)
    glb.UI_WIN.flip()           