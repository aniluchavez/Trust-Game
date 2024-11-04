import random
from os import path
from psychopy import core, event

import stimuli as stim
import globals as glb
from markEvent import markEvent


# FUNCTION THAT SHOWS THE WELCOME MESSAGE
def show_welcome():
    """Display welcome message and game instructions at the start of the experiment."""
    # Bienvenido al experimento del Juego de la Confianza. En este juego tu estaras interactuando con un companero que previamente a selecionado previamente sus respuestas.
    # Puedes escoger entre invertir o quedarte con tu dinero
    # Y tu companero puede decidir entre regresar hasta tres veces tu inversion o quedarselo
    # Presione 'ENTER' para continuar
    # Eligiendo a tus companeros ...
    # Vamos a empezar
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
#Spanish instructions: Por favor califica la confianza que le tienes a esta persona usando la escala inferior. Mueve las flechas del teclado <>
# para elegir tu grado de confianza y presiona 'ENTER'
INSTRUCTIONS_TEXT = "Please rate the trustworthiness of your partner on the scale below. Move slider with the arrow keys to desired ranking and press ENTER"
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
        stim.draw_text(f"Partner: {PartnerName}", Height=50, Pos=(0, 0))
        stim.draw_text(INSTRUCTIONS_TEXT, Pos=(0, -0.3), Height=40)
        stim.SLIDER.draw()
        # no confiable, neutral, confianble
        stim.draw_text("Not Trustworthy", Pos=(-0.4, -0.6), Height=40)
        stim.draw_text("Neutral", Pos=(0, -0.6), Height=40)
        stim.draw_text("Trustworthy", Pos=(0.4, -0.6), Height=40)
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
        stim.draw_text("Response noted.", Pos=(0, -0.9), Height=60)
        glb.UI_WIN.flip()

        markEvent(f'{EventType}End', CpuIndex)
        core.wait(1.5)

    return {'type': EventType,
            'partner': PartnerName,
            'ranking': response,
            'response_time': responseTime
            }


# FUNCTION FOR MAIN TRIAL SEQUENCE
def normal_trial(TrialIdx:int, BlockIdx:int, UserRole:str, CpuRole:str, GameLogic, CpuIndex:int, PartnerImage:str, PartnerName:str):
    GameLogic.set_fresh_pot()  # Set the fresh pot once per trial
    cpuResponse = "___"
    markEvent("trialStart", TrialIdx, BlockIdx, 'trust')
    if UserRole == "trustor":
        userDecision = normal_decision_phase(GameLogic, CpuIndex, PartnerImage, PartnerName)
        if not glb.ABORT:
            cpuResponse = normal_outcome_phase(userDecision, GameLogic, CpuIndex, PartnerName)
    else:
        cpuDecision = {"choice": "give", "amount": GameLogic.trustor_decision("give", CpuIndex)}
        cpuResponse = normal_outcome_phase(cpuDecision, GameLogic, CpuIndex, PartnerName)
        userDecision = normal_decision_phase(GameLogic, CpuIndex, PartnerImage, PartnerName)
    
    if not glb.ABORT: markEvent("trialEnd", TrialIdx, BlockIdx, 'trust')
    return {
        "trial_type": f"Trust-{UserRole}",
        "response": userDecision['choice'],
        "partner": f'{PartnerName}-{CpuRole}',
        "outcome": cpuResponse,
        "response_time": userDecision['time'],
        "misc_info": f"${userDecision['fresh_pot']} -> ${userDecision['amount']}"
    }

# FUNCTION FOR QUICK TRANSITION FROM RANKING TO START OF THE TRIAL
def show_game_start_transition():
    """Display a transition screen after the rating and before the game starts."""
    transition_text = "Starting the game. Get ready for the first trial..."
    stim.draw_text(transition_text, Pos=(0, 0), Height=50)
    glb.UI_WIN.flip()
    core.wait(2)  # Pauses for 3 seconds before starting the game

# FUNCTION TO PROCESS USER'S DECISION
def normal_decision_phase(GameLogic, CpuIndex:int, PartnerImage:str, PartnerName:str):
    # Initialize a fresh pot for this specific trial
    freshPot = GameLogic.current_fresh_pot  # Use the set fresh pot for this trial
    # Guardar , Invertir 
    keepButtonText = f"Keep ${freshPot}"
    investButtonText = f"Invest ${freshPot}"
    
    markEvent("DecisionStart")
    stim.PHOTODIODE.draw()
    norm_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText)
    core.wait(glb.PARAMETERS.timing['photodiode'])
    norm_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText)
    
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
        norm_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText, highlight)
        core.wait(glb.PARAMETERS.timing['photodiode'])
        norm_decision_draw(PartnerName, PartnerImage, keepButtonText, investButtonText, highlight)
        core.wait(glb.PARAMETERS.timing['photodiode'])
        markEvent("DecisionEnd")

    amountInvolved = GameLogic.trustor_decision(decision, CpuIndex)

    return {"choice": decision, "amount": amountInvolved, 'time': responseTime, 'fresh_pot': freshPot}

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

    outcomeMessage = ...
    outcome = ...
    if decision == "keep":
        # Tu guardaste  
        outcomeMessage = f"You kept ${amountGiven}"
        outcome = 'No Deal'
        returned_amount = 0
    else:
        #  X regreso , X se quedo con el dinero
        returned_amount = GameLogic.outcome_phase(amountGiven, CpuIndex)
        outcomeMessage = f"{PartnerName} returned ${returned_amount}" if returned_amount > 0 else f"{PartnerName} kept the money"
        outcome = 'Shared' if returned_amount > 0 else 'Kept'
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
    return outcome
# FUNCTION FOR BLOCK TRANSITIONS
def show_block_transition(block_number):
    """Display end of block message and indicate the start of the next block."""
    transition_text = f"End of Block {block_number}\n\nStarting Block {block_number + 1}...\n\nPress 'Enter' to continue."
    stim.draw_text(transition_text, Pos=(0, 0), Height=55)
    glb.UI_WIN.flip()
    event.waitKeys(keyList=['return'], maxWait=20)

# FUNCTION USED TO SIMULATE A LOTTERY TRIAL
def lottery_trial(PartnerNames:str, TrialIdx, BlockIdx):
    suggestionType = "partner" if random.random() < 0.5 else "self"
    suggestionPartner = random.choice(PartnerNames)
    # sugiere que entres a a loteria, sugiere que no entres a lo loteria, tu decide si quieres entrar a la loteria
    suggestionText = "You decide whether to enter the lottery."
    # f"{suggestionPartner} suggests you {'enter' if random.random() < 0.5 else 'do not enter'} the lottery." \
    #                      if suggestionType == "partner" else 
    response = None
    markEvent("trialStart", TrialIdx, BlockIdx, 'lottery')
    markEvent("DecisionStart")

    stim.PHOTODIODE.draw()
    lot_decision_draw(suggestionText)   
    core.wait(glb.PARAMETERS.timing['photodiode'])
    lot_decision_draw(suggestionText)     
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
        wonLottery = random.randint(0, 1) == 1
        outcome = "Won" if wonLottery else "Lost"
        # Ganaste la loteria, No ganaste la loteria
        outcomeMessage = "You won the lottery!" if wonLottery else "You did not win the lottery."
    elif 'j' in keys:
        highlight = 2
        response = "no"
        outcome = "Not Played"
        # Decidiste no entrar a la loteria
        outcomeMessage = "You chose not to play the lottery."
    
    if not glb.ABORT:
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

    return {"trial_type": "Lottery", "response": response, "partner": suggestionPartner, 
            "misc_info": suggestionText, "outcome": outcome, 'response_time': responseTime}

def lot_decision_draw(SuggestionText, Highlight=None):
    yesLine = (255,255,255) if Highlight == 1 else (0, 0, 255)
    noLine = (255,255,255) if Highlight == 2 else (0, 0, 255)

    stim.draw_image("Images/slot_machine.jpg", Pos=(0, 0.5), Size=(0.4, 0.8))
    stim.draw_text(SuggestionText, Pos=(0, -.05),Height=55, Color=(255,255,255))
    # Quieres jugar a la loteria ? 
    stim.draw_text("Do you want to play the lottery?", Pos=(0,-0.3), Height=50)
    stim.draw_rect(FillColor=(0,0,255), LineColor=yesLine, Pos=(-0.3, -0.5), Width=0.3, Height=0.15)
    stim.draw_text("Yes", Pos=(-0.3, -0.5), Height=54)
    stim.draw_rect(FillColor=(0,0,255), LineColor=noLine, Pos=(0.3, -0.5), Width=0.3, Height=0.15)
    stim.draw_text("No", Pos=(0.3, -0.5), Height=54)
    #Presiona F para Si, Presiona J para No
    stim.draw_text("Press F for Yes", Pos=(-0.3, -0.67), Height=43)
    stim.draw_text("Press J for No", Pos=(0.3, -0.67), Height=43)
    glb.UI_WIN.flip()           