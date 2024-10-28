from psychopy import visual, core, event
from stimuli import create_text_stimuli, create_button
import globals as glb
from markEvent import markEvent

class TrustGameTrial:
    def __init__(self, UI_WIN, PARAMETERS, partner_name, game_logic, user_role="trustor", cpu_role="trustee", trialIdx=0, blockIdx=0, partner_image=None):
        """
        Initialize a trial in the trust game with flexibility for user and CPU roles.

        Parameters:
        ----------
        UI_WIN : psychopy.visual.Window
            The PsychoPy window object.
        PARAMETERS : Parameters
            Experiment-wide settings and display parameters.
        partner_name : str
            Name of the partner (CPU).
        game_logic : GameLogic
            Instance of the game logic.
        user_role : str, optional
            Role of the user, defaults to 'trustor'.
        cpu_role : str, optional
            Role of the CPU, defaults to 'trustee'.
        trialIdx : int
            Index of the trial within the block.
        blockIdx : int
            Index of the block.
        partner_image : ImageStim, optional
            Partner image to display, defaults to None.
        """
        self.UI_WIN = UI_WIN
        self.PARAMETERS = PARAMETERS
        self.partner_name = partner_name
        self.game_logic = game_logic
        self.user_role = user_role
        self.cpu_role = cpu_role
        self.trialIdx = trialIdx
        self.blockIdx = blockIdx
        self.partner_image = partner_image

        # Button labels update dynamically based on trustor money
        self.button_labels = [f"Keep ${self.game_logic.trustor_money}", f"Give ${self.game_logic.trustor_money * 3}"]

        # Setup stimuli for the trial
        self.setup_stimuli()

    def setup_stimuli(self):
        """Set up visual components for the trial."""
        self.partner_name_text = create_text_stimuli(
            self.UI_WIN,
            self.PARAMETERS,
            text_content=f"Partner: {self.partner_name}",
            pos=(0, 0.7)
        )
        self.keep_button = create_button(self.UI_WIN, label=self.button_labels[0], pos=(-0.4, -0.5))
        self.give_button = create_button(self.UI_WIN, label=self.button_labels[1], pos=(0.4, -0.5))

    def show_intro(self):
        """Display introductory screen with partner's name and image."""
        self.partner_image.draw()
        self.partner_name_text.draw()
        self.UI_WIN.flip()
        core.wait(2)

    def run_trial(self):
        """Run the decision and outcome phases and log user and CPU actions."""
        glb.reset_clock()
        markEvent("trialStart", trialIdx=self.trialIdx, blockIdx=self.blockIdx)

        # Decision Phase
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

        # Log decision
        amount_given = self.game_logic.trustor_decision(decision)
        user_decision = {"choice": decision, "amount": amount_given if decision == 'give' else self.game_logic.trustor_money}
        
        decision_time = glb.ABS_CLOCK.getTime()
        markEvent("UserChoice", role=self.user_role, decision=user_decision, time=decision_time)

        # Outcome Phase
        returned_amount = self.game_logic.outcome_phase(amount_given)
        cpu_response = {"choice": "return", "amount": returned_amount} if returned_amount > 0 else {"choice": "keep", "amount": 0}

        outcome_time = glb.ABS_CLOCK.getTime()
        markEvent("OutcomeEnd", returned_amount=returned_amount, time=outcome_time)

        trial_data = {
            "trialIdx": self.trialIdx,
            "blockIdx": self.blockIdx,
            "user_decision": user_decision,
            "cpu_response": cpu_response,
            "decision_time": decision_time,
            "outcome_time": outcome_time
        }
        return trial_data
