from psychopy import core, event
from stimuli import create_general_stimuli, create_text_stimuli
from Class.game_logic import GameLogic
from markEvent import markEvent

class TrustGameTrial:
    def __init__(self, UI_WIN, PARAMETERS, partner_name, partner_image_folder, num_images, game_logic, user_role, cpu_role, trialIdx, blockIdx):
        """
        Initialize a trial in the trust game, specifying trial and block indices.
        """
        self.UI_WIN = UI_WIN
        self.PARAMETERS = PARAMETERS
        self.partner_name = partner_name
        self.game_logic = game_logic
        self.user_role = user_role
        self.cpu_role = cpu_role
        self.trialIdx = trialIdx
        self.blockIdx = blockIdx
        self.trial_data = []  # Collects data for this trial

        # Dynamic button labels based on trustor's current money amount
        self.button_labels = [f"Keep ${self.game_logic.trustor_money}", f"Give ${self.game_logic.trustor_money * 3}"]

        # Generate stimuli
        self.stimuli = create_general_stimuli(
            UI_WIN=UI_WIN,
            folder_path=partner_image_folder,
            num_images=num_images,
            PARAMETERS=PARAMETERS,
            button_labels=self.button_labels,
            overlay_text=f"Welcome to the game"
        )
        
        self.partner_name_text = create_text_stimuli(UI_WIN, PARAMETERS, self.partner_name)
        
    def log_event(self, event_name, data=None):
        """
        Logs the event with optional data and timing.
        """
        event_time = core.getTime()
        self.trial_data.append({
            'TrialIdx': self.trialIdx,
            'BlockIdx': self.blockIdx,
            'Event': event_name,
            'Data': data,
            'Time': event_time
        })
        
    def decision_phase(self):
        """
        Decision phase with event marking and data logging.
        """
        markEvent('DecisionStart', self.trialIdx + 1)
        self.log_event('DecisionPhaseStart')

        # Decision for user as trustor
        if self.user_role == 'trustor':
            self.stimuli['images'][0].draw()  # Show partner image
            self.partner_name_text.draw()
            for button in self.stimuli['buttons']:
                button.draw()
            self.UI_WIN.flip()
            
            clock = core.Clock()
            decision_made = False
            while clock.getTime() < 3 and not decision_made:
                keys = event.getKeys(['escape'])
                if 'escape' in keys:
                    core.quit()
                if self.stimuli['buttons'][0].isClicked:
                    self.participant_decision = 'keep'
                    self.game_logic.trustor_decision = 'keep'
                    markEvent("UserChoice", "keep")
                    self.log_event("UserDecision", "keep")
                    self.log_event("UserDecisionTime", clock.getTime())
                    decision_made = True
                elif self.stimuli['buttons'][1].isClicked:
                    self.participant_decision = 'give'
                    self.game_logic.trustor_decision = 'give'
                    markEvent("UserChoice", "give")
                    self.log_event("UserDecision", "give")
                    self.log_event("UserDecisionTime", clock.getTime())
                    decision_made = True
            
            if not decision_made:
                self.participant_decision = 'keep'
                markEvent("UserChoice", "keep (default)")
                self.log_event("UserDecision", "keep (default)")
                
        elif self.cpu_role == 'trustor':
            self.participant_decision = self.game_logic.cpu_trustor_decision()
            markEvent("OtherChoice", self.participant_decision)
            self.log_event("CPUDecision", self.participant_decision)
            core.wait(1)  # Simulate decision time

        markEvent('DecisionEnd', self.trialIdx + 1)
        self.log_event("DecisionPhaseEnd")
        self.UI_WIN.flip()

    def interval_phase(self):
        """
        Interval phase with event marking.
        """
        markEvent('intervalPhaseStart', self.trialIdx + 1)
        self.log_event("IntervalPhaseStart")
        core.wait(12)  # Interval time
        markEvent('intervalPhaseEnd', self.trialIdx + 1)
        self.log_event("IntervalPhaseEnd")

    def outcome_phase(self):
        """
        Outcome phase with event marking and data logging.
        """
        markEvent('OutcomeStart', self.trialIdx + 1)
        self.log_event("OutcomePhaseStart")

        if self.user_role == 'trustee':
            returned_amount = self.game_logic.trustee_decision()
            self.log_event("UserOutcome", f"Received ${returned_amount}")
        elif self.cpu_role == 'trustee':
            returned_amount = self.game_logic.cpu_trustee_decision()
            self.log_event("CPUOutcome", f"Returned ${returned_amount}")
        
        if self.participant_decision == 'keep':
            outcome_text = "You decided to keep the money."
            self.log_event("UserOutcome", "Kept the money")
        elif returned_amount == 0:
            outcome_text = f"{self.partner_name} kept the money."
            self.log_event("CPUOutcome", "Kept all money")
        else:
            outcome_text = f"{self.partner_name} shared ${returned_amount} with you."
            self.log_event("CPUOutcome", f"Shared ${returned_amount}")

        outcome_stim = create_text_stimuli(self.UI_WIN, self.PARAMETERS, outcome_text)
        outcome_stim.draw()
        self.UI_WIN.flip()
        
        markEvent('OutcomeEnd', self.trialIdx + 1)
        self.log_event("OutcomePhaseEnd")
        core.wait(1)

    def run_trial(self):
        """
        Run the full trial with phases and data logging.
        """
        markEvent('trialStart', self.trialIdx + 1, self.blockIdx + 1)
        self.log_event("TrialStart")
        self.decision_phase()
        self.interval_phase()
        self.outcome_phase()
        markEvent('trialEnd', self.trialIdx + 1, self.blockIdx + 1)
        self.log_event("TrialEnd")
        
        return self.trial_data  # Return all data collected in this trial
