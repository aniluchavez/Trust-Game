from psychopy import core, event
from stimuli import load_partner_image, create_text_stimuli, create_button, create_trust_slider
import globals as glb
from markEvent import markEvent

class TrustGameTrial:
    def __init__(self, UI_WIN, PARAMETERS, partner_name, game_logic, user_role, cpu_role, trialIdx, blockIdx, partner_image):
        self.UI_WIN = UI_WIN
        self.PARAMETERS = PARAMETERS
        self.partner_name = partner_name
        self.game_logic = game_logic
        self.user_role = user_role  # Dynamic user role
        self.cpu_role = cpu_role    # Dynamic CPU role
        self.trialIdx = trialIdx
        self.blockIdx = blockIdx
        self.partner_image = partner_image

        # Setup stimuli for the trial
        self.partner_name_text = create_text_stimuli(self.UI_WIN, self.PARAMETERS, f"Partner: {self.partner_name}", pos=(0, 0.7))
        self.trust_slider = create_trust_slider(self.UI_WIN)
        self.keep_button = create_button(self.UI_WIN, label="Keep $1", pos=(-0.4, -0.5))
        self.give_button = create_button(self.UI_WIN, label="Give $3", pos=(0.4, -0.5))
        self.outcome_text = create_text_stimuli(self.UI_WIN, self.PARAMETERS, text_content="", pos=(0, 0))

    def show_intro(self):
        """Display introductory screen with partner's name, image, and slider."""
        self.partner_image.draw()
        self.partner_name_text.draw()
        self.trust_slider.draw()
        self.UI_WIN.flip()
        core.wait(2)

    def run_decision_phase(self):
        """Decision phase where the active trustor decides to keep or give."""
        self.partner_image.draw()
        self.partner_name_text.draw()
        self.keep_button[0].draw()
        self.keep_button[1].draw()
        self.give_button[0].draw()
        self.give_button[1].draw()
        self.UI_WIN.flip()

        keys = event.waitKeys(keyList=['1', '3', 'escape'])
        if 'escape' in keys:
            core.quit()
        decision = 'keep' if '1' in keys else 'give'
        amount_given = self.game_logic.trustor_decision(decision)
        return {"choice": decision, "amount": amount_given if decision == 'give' else self.game_logic.trustor_money}

    def run_outcome_phase(self, amount_given):
        """Outcome phase where the CPU decides return based on the given amount."""
        returned_amount = self.game_logic.outcome_phase(amount_given)
        self.outcome_text.text = f"Partner returned ${returned_amount}" if returned_amount > 0 else "Partner kept the money"
        self.outcome_text.draw()
        self.UI_WIN.flip()
        core.wait(2)
        return {"choice": "return", "amount": returned_amount} if returned_amount > 0 else {"choice": "keep", "amount": 0}

    def run_trial(self):
        """Run the full sequence of intro, decision, and outcome phases."""
        glb.reset_clock()
        markEvent("trialStart", trialIdx=self.trialIdx, blockIdx=self.blockIdx)

        # Intro Phase
        self.show_intro()

        # Decision Phase
        if self.user_role == 'trustor':
            user_decision = self.run_decision_phase()
            decision_time = glb.ABS_CLOCK.getTime()
            markEvent("UserChoice", role=self.user_role, decision=user_decision, time=decision_time)
            cpu_response = self.run_outcome_phase(user_decision['amount'])
        else:
            # CPU acts as trustor, using `game_logic` to simulate the trustor's choice
            cpu_decision = self.game_logic.trustor_decision('give')
            cpu_response = self.run_outcome_phase(cpu_decision)
            user_decision = self.run_decision_phase()  # User reacts as trustee

        outcome_time = glb.ABS_CLOCK.getTime()
        markEvent("OutcomeEnd", returned_amount=cpu_response['amount'], time=outcome_time)

        # Return trial data
        return {
            "trialIdx": self.trialIdx,
            "blockIdx": self.blockIdx,
            "user_decision": user_decision,
            "cpu_response": cpu_response,
            "decision_time": decision_time,
            "outcome_time": outcome_time
        }
