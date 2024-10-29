from psychopy import core, event
from stimuli import load_partner_image, create_text_stimuli, create_button, create_trust_slider
import globals as glb
from markEvent import markEvent

class TrustGameTrial:
    def __init__(self, UI_WIN, PARAMETERS, partner_name, game_logic, user_role="trustor", cpu_role="trustee", trialIdx=0, blockIdx=0, partner_image=None):
        self.UI_WIN = UI_WIN
        self.PARAMETERS = PARAMETERS
        self.partner_name = partner_name
        self.game_logic = game_logic
        self.user_role = user_role
        self.cpu_role = cpu_role
        self.trialIdx = trialIdx
        self.blockIdx = blockIdx
        self.partner_image = partner_image

        # Initialize and set up visual components for the trial
        self.setup_stimuli()

    def setup_stimuli(self):
        """Set up visual components for the trial phases."""
        # Partner's name text stimulus
        self.partner_name_text = create_text_stimuli(
            self.UI_WIN, self.PARAMETERS, text_content=f"Partner: {self.partner_name}", pos=(0, 0)
        )
        # Trustworthiness slider for intro phase
        self.trust_slider = create_trust_slider(self.UI_WIN)
        # Decision phase buttons for Keep and Give options with dynamic labels
        self.keep_button_rect, self.keep_button_text = create_button(self.UI_WIN, label=f"Keep ${self.game_logic.trustor_money}", pos=(-0.4, -0.5))
        self.give_button_rect, self.give_button_text = create_button(self.UI_WIN, label=f"Give ${self.game_logic.trustor_money * 3}", pos=(0.4, -0.5))
        # Outcome text for outcome phase
        self.outcome_text = create_text_stimuli(self.UI_WIN, self.PARAMETERS, text_content="", pos=(0, 0))

    def show_intro(self):
        """Display introductory screen with partner's name, image, and trust slider."""
        self.partner_image.draw()  # Draw partner image
        self.partner_name_text.draw()  # Draw partner name
        self.trust_slider.draw()  # Draw slider for trust rating
        self.UI_WIN.flip()  # Flip to show all elements
        core.wait(2)  # Display intro for 2 seconds

    def run_decision_phase(self):
        """Decision phase where the user (trustor) chooses to keep or give."""
        # Update button labels based on current trustor money
        self.keep_button_text.text = f"Keep ${self.game_logic.trustor_money}"
        self.give_button_text.text = f"Give ${self.game_logic.trustor_money * 3}"

        # Draw decision phase components
        self.partner_image.draw()  # Partner image
        self.partner_name_text.draw()  # Partner name
        self.keep_button_rect.draw()  # Keep button background
        self.keep_button_text.draw()  # Keep button text
        self.give_button_rect.draw()  # Give button background
        self.give_button_text.draw()  # Give button text
        self.UI_WIN.flip()  # Flip to show all decision elements

        # Wait for user input
        keys = event.waitKeys(keyList=['1', '3', 'escape'])
        if 'escape' in keys:
            core.quit()  # Exit experiment if 'escape' is pressed
        decision = 'keep' if '1' in keys else 'give'

        # Log decision and process it in game logic
        amount_given = self.game_logic.trustor_decision(decision) if self.user_role == 'trustor' else 0
        return {"choice": decision, "amount": amount_given if decision == 'give' else self.game_logic.trustor_money}

    def run_outcome_phase(self, amount_given):
        """Outcome phase where CPU decides return based on amount given."""
        returned_amount = self.game_logic.outcome_phase(amount_given) if self.cpu_role == 'trustee' else 0
        # Update outcome text based on CPU's decision
        self.outcome_text.text = f"Partner returned ${returned_amount}" if returned_amount > 0 else "Partner kept the money"
        self.outcome_text.draw()
        self.UI_WIN.flip()
        core.wait(2)  # Display outcome for 2 seconds

        return {"choice": "return", "amount": returned_amount} if returned_amount > 0 else {"choice": "keep", "amount": 0}

    def run_trial(self):
        """Run intro, decision, and outcome phases and return trial data."""
        glb.reset_clock()
        markEvent("trialStart", trialIdx=self.trialIdx, blockIdx=self.blockIdx)

        # Intro Phase - Display only on the first trial of each block
        if self.trialIdx == 0:
            self.show_intro()

        # Decision Phase
        user_decision = self.run_decision_phase()
        decision_time = glb.ABS_CLOCK.getTime()
        markEvent("UserChoice", role=self.user_role, decision=user_decision, time=decision_time)

        # Outcome Phase
        cpu_response = self.run_outcome_phase(user_decision['amount'])
        outcome_time = glb.ABS_CLOCK.getTime()
        markEvent("OutcomeEnd", returned_amount=cpu_response['amount'], time=outcome_time)

        # Return trial data
        return {
            "trialIdx": self.trialIdx,
            "blockIdx": self.blockIdx,
            "user_role": self.user_role,
            "cpu_role": self.cpu_role,
            "user_decision": user_decision,
            "cpu_response": cpu_response,
            "decision_time": decision_time,
            "outcome_time": outcome_time
        }
