import random
from os import path

from psychopy import core, event

import stimuli as stim
import globals as glb
from markEvent import markEvent



# FUNCTION THAT SHOWS THE WELCOME MESSAGE
def show_welcome():
    """Display welcome message and game instructions at the start of the experiment."""
    
    # Generate and draw the instructions
    welcomeText = "Welcome to the Trust Game Experiment!\n\nIn this game, you'll be interacting with a partner that precorded their responses.\n\n "+\
                   "You are the trustor and start with $1 in your account.\n"+\
                   "You can choose to keep or give money, and your partner may choose to share some amount back or keep it all for themselves.\n\n"+\
                   "Press 'Enter' to continue."
    stim.draw_text(welcomeText, Pos=(0,0), Height=40)
    glb.UI_WIN.flip()
        
    # Wait for Enter key to confirm
    event.waitKeys(keyList=['return'], maxWait=20)

    # Briefly display a message to confirm the start of the experiment
    confirmationText="Let's begin!"
    stim.draw_text(confirmationText, Height=50, Pos=(0,0))

    # Clear the screen before proceeding
    glb.UI_WIN.flip()
    core.wait(3)




# FUNCTION THAT PROMPTS THE PARTICIPANT TO RATE THE TRUSTWORTHINESS OF AN INDIVIDUAL
# Arguments: 
#   PartnerImage:   The filename for the image of the partner
#   PartnerName:    The name of the partner
#   EventType:      Type of event to identify the stage of the task that we are in
# Returns:
#   response:       The player's trust rating
INSTRUCTIONS_TEXT = "Please rate the trustworthiness of your partner on the scale below. Move slider with trackpad to desired ranking and press ENTER"
def show_trust_ranking(PartnerImage:str, PartnerName:str, EventType:str):
    # Reset the trust slider
    stim.SLIDER.reset()
    # instructionsText = "Please rate the trustworthiness of your partner on the scale below. Move slider with trackpad to desired ranking and press ENTER"
    # skipRender=False
    # previousRating = None
    response = None         # Record the response
    partnerImageName = path.join(glb.PARAMETERS.stimuli['imageFolder'], PartnerImage)      # Generate the path to the image
    while response is None:
        stim.draw_image(partnerImageName, Pos= (0,0.5), Size=(0.8,0.8))     # Draw the Partner image
        stim.draw_text(f"Partner: {PartnerName}",Height=50, Pos=(0,0))      # Draw the Partner's name
        stim.draw_text(INSTRUCTIONS_TEXT, Pos=(0, -0.3), Height=40)         # Draw the instructions
        stim.SLIDER.draw()                                                  # Draw the trust slider
        stim.draw_text("Not Trustworthy", Pos=(-0.4, -0.6), Height=40)      # Draw the leftmost label
        stim.draw_text("Neutral", Pos=(0,-0.6), Height=40)                  # Draw the middle label
        stim.draw_text("Trustworthy", Pos=(0.4, -0.6), Height=40)           # Draw the rightmost label
        glb.UI_WIN.flip()  
            
        # if previousRating != stim.SLIDER.getRating():
        #     previousRating =  stim.SLIDER.getRating()
        #     skipRender = False
        # print(previousRating, stim.SLIDER.getRating())

        # If the user presses enter, record their response
        keys = event.getKeys(keyList=['return'])
        if 'return' in keys:
            response = stim.SLIDER.getRating() or 5
            markEvent(EventType, rating=response, time=glb.ABS_CLOCK.getTime()) 
    
    # Draw the experiment after it is done
    stim.draw_image(partnerImageName, Pos= (0,0.5), Size=(0.8,0.8))     # Draw the Partner image
    stim.draw_text(f"Partner: {PartnerName}", Pos=(0,0), Height=50)     # Draw the Partner's name
    stim.SLIDER.draw()                                                  # Draw the trust slider and its response
    stim.draw_text("Not Trustworthy", Pos=(-0.4, -0.6), Height=40)      # Draw the leftmost label
    stim.draw_text("Neutral", Pos=(0,-0.6), Height=40)                  # Draw the middle label
    stim.draw_text("Trustworthy", Pos=(0.4, -0.6), Height=40)           # Draw the rightmost label
    stim.draw_text("Response noted.", Pos=(0, -0.9), Height=60)         # Draw that the response was received
    glb.UI_WIN.flip()  

    # Wait for some time
    core.wait(3) 
    return response




# FUNCTION THAT ASKS THE PARTICIPANT TO KEEP OR INVEST
# Arguments:
#   TrialIdx:       The index of the current trial
#   BlockIdx:       The index of the current block
#   UserRole:       The role of the participant
#   CpuRole:        The role of the CPU
#   GameLogic:      The parameters and logic that will be followed in this trial
#   CpuIndex:       The index of the Cpu
#   PartnerImage:   The filename of the image that represents the CPU/partner
#   PartnerName:    The personalized name given to the CPU/partner
# Returns:
#   Dictionary Containing: Trial Index, Block Index, Participant's Role, CPU's Role, Participant's Decision, CPU's Decision
def normal_trial(TrialIdx:int, BlockIdx:int, UserRole:str, CpuRole:str, GameLogic, CpuIndex:int, PartnerImage:str, PartnerName:str):
    glb.reset_clock()       # Reset the clock (idk why)

    markEvent("trialStart", trialIdx=TrialIdx, blockIdx=BlockIdx) # Mark the start of the trial
    # Act on whether the user is a trustor (decision->outcome) or a trustee (outcome->decision)
    if UserRole == "trustor":
        userDecision = normal_decision_phase(GameLogic, CpuIndex, PartnerImage, PartnerName)
        decision_time = glb.ABS_CLOCK.getTime()
        markEvent("UserChoice", role=UserRole, decision=userDecision["choice"], time=decision_time)
        cpu_response = normal_outcome_phase(userDecision, GameLogic, CpuIndex, PartnerName)
        outcome_time = glb.ABS_CLOCK.getTime()
        markEvent("OutcomeEnd", returned_amount=cpu_response["amount_returned"], time=outcome_time)
        
    else:
        cpuDecision = {"choice": "give", "amount": GameLogic.trustor_decision("give", CpuIndex)}
        cpu_response = normal_outcome_phase(cpuDecision, GameLogic, CpuIndex, PartnerName)
        userDecision = normal_decision_phase(GameLogic, CpuIndex, PartnerImage, PartnerName)
        markEvent("UserChoice", role=UserRole, decision=userDecision["choice"])
    return {
        "trialIdx": TrialIdx,
        "blockIdx": BlockIdx,
        "user_role": UserRole,
        "cpu_role": CpuRole,
        "user_decision": userDecision,
        "cpu_response": cpu_response,
    }


# FUNCTION USED BY normal_trial() FOR ALLOWING THE PARTICIPANT TO DECIDE ON WHETHER TO KEEP OR INVEST
# Arguments:
#   GameLogic:      The parameters and logic that will be followed in this trial
#   CpuIndex:       The index of the Cpu
#   PartnerImage:   The filename of the image that represents the CPU/partner
#   PartnerName:    The personalized name given to the CPU/partner
# Returns:
#   Dictionary containing: The user's decision and the amount of money involved
def normal_decision_phase(GameLogic, CpuIndex:int, PartnerImage:str, PartnerName:str):
    # Display the same amount for both keep and invest
    currentBalanceDisplay = GameLogic.trustor_balances[CpuIndex]
    keepButtonText = f"Keep ${currentBalanceDisplay}"
    investButtonText = f"Invest ${currentBalanceDisplay}"

    # Draw the prompt
    stim.draw_image(path.join(glb.PARAMETERS.stimuli['imageFolder'], PartnerImage), Pos= (0,0.5), Size=(0.8,0.8)) # Draw the image of the partner
    stim.draw_text(f"Partner: {PartnerName}", Pos=(0,0), Height=50)                                               # Draw the name of the partner
    stim.draw_rect(FillColor=(0,0,255), LineColor=(0,0,255), Width=0.6, Height=0.2, Pos=(-0.4, -0.5))             # Draw the box for the keep text
    stim.draw_text(keepButtonText, Pos=(-0.4, -0.5), Height=60)                                                   # Draw the keep text
    stim.draw_rect(FillColor=(0,0,255), LineColor=(0,0,255), Width=0.6, Height=0.2, Pos=(0.4, -0.5))              # Draw the box for the invest text
    stim.draw_text(investButtonText, Pos=(0.4, -0.5), Height=60)                                                  # Draw the invest text
    stim.draw_text("Press '1' to Keep", Pos=(-0.4, -0.7), Height=54)                                              # Draw the button 1 text
    stim.draw_text("Press '3' to Invest", Pos=(0.4, -0.7), Height=54)                                             # Draw the button 3 text
    glb.UI_WIN.flip()

    # Wait for the key to be pressed
    keys = event.waitKeys(keyList=['1', '3', 'escape'])
    if 'escape' in keys:
        core.quit()
    decision = 'keep' if '1' in keys else 'invest'
        
    # Call the game logic with the actual decision
    amount_involved = GameLogic.trustor_decision(decision, CpuIndex)

    return {"choice": decision, "amount": amount_involved}


# FUNCTION USED BY normal_trial() FOR DISPLAYING THE OUTCOME OF THE PARTICIPANT'S OR CPU'S DECISION
# Arguments:
#   DecisionData:   The data for the participant's OR CPU's decision
#   GameLogic:      The parameters and logic that will be followed in this trial
#   CpuIndex:       The index of the Cpu
#   PartnerName:    The personalized name given to the CPU/partner
# Returns:
#   Dictionary containing: The user's decision and the amount of money involved
def normal_outcome_phase(DecisionData:dict, GameLogic, CpuIndex:int, PartnerName:int):
    # Extract the decision data
    decision = DecisionData["choice"]
    amountGiven = DecisionData["amount"]
    
    # Calculate the outcome message
    outcomeMessage = ...
    if decision == "keep":
        outcomeMessage = f"You kept ${amountGiven}"
    else:
        returned_amount = GameLogic.outcome_phase(amountGiven, CpuIndex)
        if returned_amount > 0:
            outcomeMessage = f"{PartnerName} returned ${returned_amount}"
        else:
            outcomeMessage = f"{PartnerName} kept the money"
            if GameLogic.trustor_balances[CpuIndex] == GameLogic.initial_money:
                outcomeMessage += f" (Your balance was replenished to ${GameLogic.initial_money})"

    # Draw outcome display
    stim.draw_rect(FillColor=(0,0,255), Width=0.99, Height=0.4, Pos=(0,0))  # Draw the box for the outcome text
    stim.draw_text(outcomeMessage, Pos=(0,0), Height=80)                    # Draw the outcome text
    glb.UI_WIN.flip()
    
    # Wait
    core.wait(2)

    return {
        "choice": decision,
        "amount_given": amountGiven if decision == "invest" else 0,
        "amount_returned": returned_amount if decision == "invest" else 0
    }




# FUNCTION USED TO SIMULATE A LOTTERY TRIAL
# Arguments:
#   PartnerNames:       The names of all the partners
# Returns:
#   Dictionary containing: trial type, user's response, suggestion text
YES_POS = (-0.3, -0.5)
NO_POS = (0.3, -0.5)
def lottery_trial(PartnerNames:str):
    # SUGGESTION STEP - GENERATE A RANDOM SUGGESTION WITH A RANDOM PARTNER
    suggestionText = ...
    suggestionType = "partner" if random.random() < 0.5 else "self"
    if suggestionType == "partner":
        partner_name = random.choice(PartnerNames)
        suggestion = random.choice(["enter", "do not enter"])
        suggestionText = f"{partner_name} suggests you {suggestion} the lottery."
    else:
        suggestionText = "You decide whether to enter the lottery."

    response = None

    # DECISION PHASE - DRAW THE PROMPT FOR THE DECISION
    stim.draw_image("Images/slot_machine.jpg", Pos=(0, 0.5), Size=(0.5, 0.8))       # Draw the slot machine
    stim.draw_text(suggestionText, Pos=(0, -.05), Color=(255,255,255))              # Draw the partner's/CPU's random suggestion text
    stim.draw_text("Do you want to play the lottery?", Pos=(0,-0.3), Height=50)     # Draw the question prompt text
    stim.draw_rect(FillColor=(0,0,255), Pos=YES_POS, Width=0.3, Height=0.15)        # Draw the box for the 'Yes' prompt
    stim.draw_text("Yes", Pos= YES_POS, Height=54)                                  # Draw the 'Yes' prompt
    stim.draw_rect(FillColor=(0,0,255), Pos=NO_POS, Width=0.3, Height=0.15)         # Draw the box for the 'No' prompt
    stim.draw_text("No", Pos=NO_POS, Height=54)                                     # Draw the 'No' prompt
    stim.draw_text("Press 1 for Yes", Pos=(-0.3, -0.67), Height=43)                 # Draw the button 1 instructions
    stim.draw_text("Press 3 for No", Pos=(0.3, -0.67), Height=43)                   # Draw the button 3 instructions
    glb.UI_WIN.flip()                        

    # Wait for user input
    keys = event.waitKeys(keyList=['1', '3', 'escape'])
    outcomeMessage = 'ABORT'
    if 'escape' in keys:
        core.quit()
    elif '1' in keys:
        response = "yes"
        wonLottery = random.randint(0, 1) == 1  # 50% chance to win
        outcomeMessage = "You won the lottery!" if wonLottery else "You did not win the lottery."
    elif '3' in keys:
        response = "no"
        outcomeMessage = "You chose not to play the lottery."

    # OUTCOME PHASE
    stim.draw_rect(FillColor=(0,0,255), Width=0.9, Height=0.4, Pos=(0,0))       # Draw a box for the text     
    stim.draw_text(outcomeMessage, Height=54)                                   # Draw the ourcome text
    glb.UI_WIN.flip()

    # Wait
    core.wait(2)

    return {"trial_type": "lottery", "response": response, "suggestion_text":suggestionText}