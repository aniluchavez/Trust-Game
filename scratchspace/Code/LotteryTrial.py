import random
from random import choice, randint
# from stimuli import create_text_stimuli
import globals as glb
from markEvent import markEvent
from psychopy.visual import TextStim, ImageStim,Rect
from psychopy import core, event, visual

class LotteryTrial:
    def __init__(self, UI_WIN, PARAMETERS, game_logic, partner_names, trialIdx, blockIdx):
        self.UI_WIN = UI_WIN
        self.PARAMETERS = PARAMETERS
        self.game_logic = game_logic
        self.partner_names = partner_names
        self.trialIdx = trialIdx
        self.blockIdx = blockIdx
        self.setup_stimuli()

    def setup_stimuli(self):
        """Set up the lottery trial stimuli, including the choice buttons and texts."""
        # Slot machine image at the top center
        self.slot_machine_image = ImageStim(self.UI_WIN, image="Images/slot_machine.jpg", pos=(0, 0.5), size=(0.5, 0.8))

        # Blue rectangles for Yes and No choices
        self.yes_rect = Rect(self.UI_WIN, width=0.3, height=0.15, fillColor='blue', pos=(-0.3, -0.5))
        self.no_rect = Rect(self.UI_WIN, width=0.3, height=0.15, fillColor='blue', pos=(0.3, -0.5))

        # Overlayed text for Yes and No
        self.yes_text = TextStim(self.UI_WIN, text="Yes", pos=self.yes_rect.pos, color="white", height=0.1)
        self.no_text = TextStim(self.UI_WIN, text="No", pos=self.no_rect.pos, color="white", height=0.1)

        # Partner suggestion text
        self.suggestion_text = TextStim(self.UI_WIN, text="", pos=(0, -.05), color="white", height=0.1)

        # Lottery decision question text
        self.lottery_decision_text = TextStim(self.UI_WIN, text="Do you want to play the lottery?", pos=(0, -0.3), color="white", height=0.09)

        # Instructions text for buttons
        self.instructions_text_1 = TextStim(self.UI_WIN, text="Press 1 for Yes", pos=(-.3, -0.67), color="white", height=0.08)
        self.instructions_text_3 = TextStim(self.UI_WIN, text="Press 3 for No", pos=(.3, -0.67), color="white", height=0.08)

    def setup_suggestion(self):
        """Randomly assign partner suggestion or self-guided prompt and set the suggestion text."""
        suggestion_type = "partner" if random.random() < 0.5 else "self"
        if suggestion_type == "partner":
            partner_name = choice(self.partner_names)
            suggestion = choice(["enter", "not enter"])
            self.suggestion_text.text = f"{partner_name} suggests you {'enter' if suggestion == 'enter' else 'not enter'} the lottery."
        else:
            self.suggestion_text.text = "You decide whether to enter the lottery."

    def run_decision_phase(self):
        """Present partner suggestion (if applicable) and lottery decision prompt, and record choice."""
        response = None
        while response is None:
            # Draw all elements in the decision phase
            self.slot_machine_image.draw()               # Slot machine image
            self.suggestion_text.draw()                  # Suggestion text
            self.lottery_decision_text.draw()            # Decision question
            self.yes_rect.draw()                         # Yes button
            self.no_rect.draw()                          # No button
            self.yes_text.draw()
            self.no_text.draw()
            self.instructions_text_1.draw() 
            self.instructions_text_3.draw()               # Button instructions
            self.UI_WIN.flip()                           # Display all elements

            # Wait for user input
            keys = event.waitKeys(keyList=['1', '3', 'escape'])
            if 'escape' in keys:
                core.quit()
            elif '1' in keys:
                response = "yes"
            elif '3' in keys:
                response = "no"

        return response

    def run_outcome_phase(self, decision):
        """Determine lottery outcome and display result."""
        if decision == "yes":
            won_lottery = randint(0, 1) == 1  # 50% chance to win
            outcome_message = "You won the lottery!" if won_lottery else "You did not win the lottery."
        else:
            outcome_message = "You chose not to play the lottery."

        outcome_background = Rect(self.UI_WIN, width=0.9, height=0.4, fillColor='blue', pos=(0, 0))
        outcome_text = TextStim(self.UI_WIN, text=outcome_message, pos=(0, 0), color="white", height=0.1)
        #self.slot_machine_image.draw()
        outcome_background.draw()  # Draw slot machine image again for outcome display
        outcome_text.draw()
        self.UI_WIN.flip()
        core.wait(2)

    def run_trial(self):
        """Run the lottery trial, presenting the option to play the lottery."""
        self.setup_suggestion()  # Set up partner suggestion or self-prompt

        # Run the decision phase
        decision = self.run_decision_phase()

        # Run the outcome phase based on the decision
        self.run_outcome_phase(decision)
        return {"trial_type": "lottery", "response": decision, "suggestion_text": self.suggestion_text.text}
