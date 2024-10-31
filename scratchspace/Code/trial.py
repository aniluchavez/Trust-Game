import random
from os import path

from psychopy import core, event
# from stimuli import create_text_stimuli, create_button, create_trust_slider
# from psychopy.visual import TextStim, Rect

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
        stim.draw_slider()                                                  # Draw the trust slider
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
    stim.draw_slider()                                                  # Draw the trust slider and its response
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
#   TrialIdx:       
def normal_trial(TrialIdx, BlockIdx, UserRole, CpuRole, GameLogic, CpuIndex, PartnerImage, PartnerName):
    glb.reset_clock()
    markEvent("trialStart", trialIdx=TrialIdx, blockIdx=BlockIdx)
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

def normal_decision_phase(GameLogic, CpuIndex, PartnerImage, PartnerName):
    # Display the same amount for both keep and invest
        currentBalanceDisplay = GameLogic.trustor_balances[CpuIndex]
        keepButtonText = f"Keep ${currentBalanceDisplay}"
        investButtonText = f"Invest ${currentBalanceDisplay}"

        stim.draw_image(path.join(glb.PARAMETERS.stimuli['imageFolder'], PartnerImage), Pos= (0,0.5), Size=(0.8,0.8))
        stim.draw_text(f"Partner: {PartnerName}", Pos=(0,0))
        stim.draw_rect(FillColor=(0,0,255), LineColor=(0,0,255), Width=0.6, Height=0.2, Pos=(-0.4, -0.5))
        stim.draw_text(keepButtonText, Pos=(-0.4, -0.5), Height=60)
        stim.draw_rect(FillColor=(0,0,255), LineColor=(0,0,255), Width=0.6, Height=0.2, Pos=(0.4, -0.5))
        stim.draw_text(investButtonText, Pos=(0.4, -0.5), Height=60)
        stim.draw_text("Press '1' to Keep", Pos=(-0.4, -0.7), Height=54)
        stim.draw_text("Press '3' to Invest", Pos=(0.4, -0.7), Height=54)
        glb.UI_WIN.flip()

        keys = event.waitKeys(keyList=['1', '3', 'escape'])
        if 'escape' in keys:
            core.quit()
        decision = 'keep' if '1' in keys else 'invest'
        
        # Call the game logic with the actual decision
        amount_involved = GameLogic.trustor_decision(decision, CpuIndex)
        return {"choice": decision, "amount": amount_involved}

def normal_outcome_phase(DecisionData, GameLogic, CpuIndex, PartnerName):
    decision = DecisionData["choice"]
    amountGiven = DecisionData["amount"]
    
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
    stim.draw_rect(FillColor=(0,0,255), Width=0.99, Height=0.4, Pos=(0,0))
    stim.draw_text(outcomeMessage, Pos=(0,0), Height=80)
    glb.UI_WIN.flip()
    core.wait(2)

    return {
        "choice": decision,
        "amount_given": amountGiven if decision == "invest" else 0,
        "amount_returned": returned_amount if decision == "invest" else 0
    }


def lottery_trial(PartnerNames):
    """Run the lottery trial, presenting the option to play the lottery."""
    ## SUGGESTION STEP
    suggestionText = ...
    suggestionType = "partner" if random.random() < 0.5 else "self"
    if suggestionType == "partner":
        partner_name = random.choice(PartnerNames)
        suggestion = random.choice(["enter", "do not enter"])
        suggestionText = f"{partner_name} suggests you {suggestion} the lottery."
    else:
        suggestionText = "You decide whether to enter the lottery."

    """Present partner suggestion (if applicable) and lottery decision prompt, and record choice."""
    response = None

    # DECISION PHASE
    yesRectPos = (-0.3, -0.5)
    noRectPos = (0.3, -0.5)
    stim.draw_image("Images/slot_machine.jpg", Pos=(0, 0.5), Size=(0.5, 0.8))
    stim.draw_text(suggestionText, Pos=(0, -.05), Color=(255,255,255))
    stim.draw_text("Do you want to play the lottery?", Pos=(0,-0.3), Height=50)
    stim.draw_rect(FillColor=(0,0,255), Pos=yesRectPos, Width=0.3, Height=0.15)
    stim.draw_text("Yes", Pos= yesRectPos, Height=54)                         # Yes button
    stim.draw_rect(FillColor=(0,0,255), Pos=noRectPos, Width=0.3, Height=0.15)
    stim.draw_text("No", Pos=noRectPos, Height=54)
    stim.draw_text("Press 1 for Yes", Pos=(-0.3, -0.67), Height=43)
    stim.draw_text("Press 3 for No", Pos=(0.3, -0.67), Height=43)
    glb.UI_WIN.flip()                           # Display all elements

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
    stim.draw_rect(FillColor=(0,0,255), Width=0.9, Height=0.4, Pos=(0,0))
    stim.draw_text(outcomeMessage, Height=54)
    glb.UI_WIN.flip()
    core.wait(2)

    return {"trial_type": "lottery", "response": response, "suggestion_text":suggestionText}

# class TrustGameTrial:
#     def __init__(self, UI_WIN, PARAMETERS, partner_name, game_logic, cpu_index=0, user_role="trustor", cpu_role="trustee", trialIdx=0, blockIdx=0, partner_image=None):
#         self.UI_WIN = UI_WIN
#         self.PARAMETERS = PARAMETERS
#         self.partner_name = partner_name
#         self.game_logic = game_logic
#         self.cpu_index = cpu_index
#         self.user_role = user_role
#         self.cpu_role = cpu_role
#         self.trialIdx = trialIdx
#         self.blockIdx = blockIdx
#         self.partner_image = partner_image
#         self.intro_displayed = False
#         self.setup_stimuli()

#     def setup_stimuli(self):
#         if not hasattr(self, 'partner_name_text'):
#             self.partner_name_text = create_text_stimuli(
#                 self.UI_WIN, self.PARAMETERS, f"Partner: {self.partner_name}", pos=(0, 0)
#             )
#         if not hasattr(self, 'trust_slider'):
#             self.trust_slider, self.instructions_text, self.not_trustworthy_label, self.neutral_label, self.trustworthy_label = create_trust_slider(self.UI_WIN)

#         if self.game_logic is not None:
#             if not hasattr(self, 'keep_button_rect'):
#                 self.keep_button_rect, self.keep_button_text = create_button(
#                     self.UI_WIN, label=f"Keep ${self.game_logic.trustor_balances[self.cpu_index]}", pos=(-0.4, -0.5)
#                 )
#             if not hasattr(self, 'invest_button_rect'):
#                 self.invest_button_rect, self.invest_button_text = create_button(
#                     self.UI_WIN, label=f"Invest ${self.game_logic.trustor_balances[self.cpu_index]}", pos=(0.4, -0.5)
#                 )

#         if not hasattr(self, 'outcome_text'):
#             self.outcome_text = create_text_stimuli(self.UI_WIN, self.PARAMETERS, text_content="", pos=(0, 0))
#         if not hasattr(self, 'decision_instruction_text_1'):
#             self.decision_instruction_text_1 = create_text_stimuli(
#                 self.UI_WIN, self.PARAMETERS, "Press '1' to Keep", pos=(-.4, -.7)
#             )
#         if not hasattr(self, 'decision_instruction_text_3'):
#             self.decision_instruction_text_3 = create_text_stimuli(
#                 self.UI_WIN, self.PARAMETERS, "Press '3' to Invest", pos=(.4, -.7)
#             )
#         if not hasattr(self, 'response_recorded_text'):
#             self.response_recorded_text = create_text_stimuli(
#                 self.UI_WIN, self.PARAMETERS, "Response noted.", pos=(0, -0.9)
#             )

#     def show_block_ranking(self):
#         self.trust_slider.reset()
#         response = None
#         while response is None:
#             self.partner_image.draw()
#             self.partner_name_text.draw()
#             self.instructions_text.draw()
#             self.trust_slider.draw()
#             self.not_trustworthy_label.draw()
#             self.neutral_label.draw()
#             self.trustworthy_label.draw()
#             self.UI_WIN.flip()

#             keys = event.getKeys(keyList=['return'])
#             if 'return' in keys:
#                 response = self.trust_slider.getRating() or 5
#                 markEvent("BlockEndRanking", rating=response, time=glb.ABS_CLOCK.getTime())

#         for _ in range(30):
#             self.partner_image.draw()
#             self.partner_name_text.draw()
#             self.trust_slider.draw()
#             self.not_trustworthy_label.draw()
#             self.neutral_label.draw()
#             self.trustworthy_label.draw()
#             self.response_recorded_text.draw()
#             self.UI_WIN.flip()

#         return response

#     def show_welcome(self):
#         welcome_text = TextStim(
#             win=self.UI_WIN,
#             text="Welcome to the Trust Game!\n\nIn this game, you'll interact with multiple partners.\n\n"
#                 "Choose to keep or invest your money with your partner, and see if they invest back!\n\n"
#                 "Press 'Enter' to continue.",
#             pos=(0, 0),
#             height=0.1,
#             wrapWidth=1.5
#         )

#         # Draw welcome text and wait for "Enter" key
#         response = None
#         while response is None:
#             welcome_text.draw()
#             self.UI_WIN.flip()
#             keys = event.getKeys(keyList=['return'])
#             if 'return' in keys:
#                 response = True

#         # Show confirmation message before starting
#         confirmation_text = TextStim(
#             win=self.UI_WIN,
#             text="Let's begin!",
#             pos=(0, 0),
#             height=0.4
#         )
        
#         for _ in range(30):  # Display for a short duration
#             confirmation_text.draw()
#             self.UI_WIN.flip()
#         self.UI_WIN.flip()  # Clear screen after confirmation
#         core.wait(1)

#     def show_intro(self):
#         if self.intro_displayed:
#             return
#         self.intro_displayed = True

#         self.trust_slider.reset()
#         response = None
#         while response is None:
#             self.partner_image.draw()
#             self.partner_name_text.draw()
#             self.instructions_text.draw()
#             self.trust_slider.draw()
#             self.not_trustworthy_label.draw()
#             self.neutral_label.draw()
#             self.trustworthy_label.draw()
#             self.UI_WIN.flip()

#             keys = event.getKeys(keyList=['return'])
#             if 'return' in keys:
#                 response = self.trust_slider.getRating() or 5
#                 markEvent("IntroSlider", rating=response, time=glb.ABS_CLOCK.getTime())

#         for _ in range(30):
#             self.partner_image.draw()
#             self.partner_name_text.draw()
#             self.trust_slider.draw()
#             self.not_trustworthy_label.draw()
#             self.neutral_label.draw()
#             self.trustworthy_label.draw()
#             self.response_recorded_text.draw()
#             self.UI_WIN.flip()

#         return response
    
#     def run_decision_phase(self):
#         # Display the same amount for both keep and invest
#         current_balance_display = self.game_logic.trustor_balances[self.cpu_index]
#         self.keep_button_text.text = f"Keep ${current_balance_display}"
#         self.invest_button_text.text = f"Invest ${current_balance_display}"

#         self.partner_image.draw()
#         self.partner_name_text.draw()
#         self.keep_button_rect.draw()
#         self.keep_button_text.draw()
#         self.invest_button_rect.draw()
#         self.invest_button_text.draw()
#         self.decision_instruction_text_1.draw()
#         self.decision_instruction_text_3.draw()
#         self.UI_WIN.flip()

#         keys = event.waitKeys(keyList=['1', '3', 'escape'])
#         if 'escape' in keys:
#             core.quit()
#         decision = 'keep' if '1' in keys else 'invest'
        
#         # Call the game logic with the actual decision
#         amount_involved = self.game_logic.trustor_decision(decision, self.cpu_index)
#         return {"choice": decision, "amount": amount_involved}

#     def run_outcome_phase(self, decision_data):
#         decision = decision_data["choice"]
#         amount_given = decision_data["amount"]

#         if decision == "keep":
#             outcome_message = f"You kept ${amount_given}"
#         else:
#             returned_amount = self.game_logic.outcome_phase(amount_given, self.cpu_index)
#             if returned_amount > 0:
#                 outcome_message = f"{self.partner_name} returned ${returned_amount}"
#             else:
#                 outcome_message = f"{self.partner_name} kept the money"
#                 if self.game_logic.trustor_balances[self.cpu_index] == self.game_logic.initial_money:
#                     outcome_message += f" (Your balance was replenished to ${self.game_logic.initial_money})"

#         # Draw outcome display
#         trial_outcome_background = Rect(self.UI_WIN, width=0.99, height=0.4, fillColor='blue', pos=(0, 0))
#         trial_outcome_background.draw()
#         self.outcome_text.text = outcome_message
#         self.outcome_text.draw()
#         self.UI_WIN.flip()
#         core.wait(2)

#         return {
#             "choice": decision,
#             "amount_given": amount_given if decision == "invest" else 0,
#             "amount_returned": returned_amount if decision == "invest" else 0
#         }
    



#     def run_trial(self):
#         glb.reset_clock()
#         markEvent("trialStart", trialIdx=self.trialIdx, blockIdx=self.blockIdx)

#         if self.user_role == "trustor":
#             user_decision = self.run_decision_phase()
#             decision_time = glb.ABS_CLOCK.getTime()
#             markEvent("UserChoice", role=self.user_role, decision=user_decision["choice"], time=decision_time)

#             cpu_response = self.run_outcome_phase(user_decision)
#             outcome_time = glb.ABS_CLOCK.getTime()
#             markEvent("OutcomeEnd", returned_amount=cpu_response["amount_returned"], time=outcome_time)
            
#         else:
#             cpu_decision = {"choice": "give", "amount": self.game_logic.trustor_decision("give", self.cpu_index)}
#             cpu_response = self.run_outcome_phase(cpu_decision)

#             user_decision = self.run_decision_phase()
#             markEvent("UserChoice", role=self.user_role, decision=user_decision["choice"])

#         return {
#             "trialIdx": self.trialIdx,
#             "blockIdx": self.blockIdx,
#             "user_role": self.user_role,
#             "cpu_role": self.cpu_role,
#             "user_decision": user_decision,
#             "cpu_response": cpu_response,
#         }
