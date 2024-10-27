from random import choice, uniform
from psychopy import core, visual, event
import random

from random import choice, uniform, choices
from psychopy import core, visual, event
import random

class CPU:
    def __init__(self, trustworthiness='trustworthy', weights=None):
        """
        CPU behavior based on trustworthiness level and weighted sampling.
        
        Parameters:
        ----------
        trustworthiness : str
            Level of trustworthiness ('trustworthy', 'untrustworthy').
        weights : dict, optional
            Probability weights for each subrange. Defaults are defined for each trust level.
        """
        self.trustworthiness = trustworthiness
        
        # Set default weights if not provided
        if weights is None:
            if self.trustworthiness == 'trustworthy':
                self.weights = {'low': 0.2, 'high': 0.8}  # More likely to return from 0.6-0.9
            else:
                self.weights = {'low': 0.8, 'high': 0.2}  # More likely to return from 0.0-0.6
        else:
            self.weights = weights

    def decide_return(self, received_amount):
        """
        CPU decides how much to return based on trustworthiness using weighted sampling.
        
        Parameters:
        ----------
        received_amount : int
            Amount the trustee (CPU) received from the trustor.
            
        Returns:
        --------
        int
            Amount the CPU decides to return.
        """
        # Define the subranges
        low_range = uniform(0.0, 0.6)  # Low range 0-0.6X
        high_range = uniform(0.6, 0.9)  # High range 0.6-0.9X
        
        # Choose a subrange based on weights
        chosen_range = choices([low_range, high_range], weights=[self.weights['low'], self.weights['high']])[0]
        
        # Return the amount to be given back
        return int(received_amount * chosen_range)

    def keep_money(self, returned_amount):
        """
        Check if the trustee decided to keep all the money.
        
        Parameters:
        ----------
        returned_amount : int
            The amount the trustee decided to return.
            
        Returns:
        --------
        bool
            True if the trustee kept all the money (i.e., returned 0).
        """
        return returned_amount == 0


class GameLogic:
    def __init__(self, UI_WIN, trustworthiness='trustworthy', initial_money=3, weights=None):
        """
        Initialize the game logic with specific trustee behavior and initial money.
        
        Parameters:
        ----------
        UI_WIN : psychopy.visual.Window
            The window to display stimuli.
        trustworthiness : str
            The trustworthiness of the trustee ('trustworthy' or 'untrustworthy').
        initial_money : int
            Initial amount of money for the trustor.
        weights : dict, optional
            Probability weights for each subrange. Defaults to trust level-based weights.
        """
        self.UI_WIN = UI_WIN
        self.trustor_money = initial_money
        self.trustee_money = 0  # Trustee starts with nothing
        self.decision = None
        self.cpu = CPU(trustworthiness=trustworthiness, weights=weights)  # Assign trustworthiness level to CPU
    
    def assign_role(self):
        """
        For now randomly assign the user a role: trustor or trustee. 
        """
        self.role = choice(['trustor', 'trustee'])
        return self.role

    def trustor_decision(self):
        """
        Decision phase for the trustor: Keep or give 3X to the trustee.
        """
        decision_text = visual.TextStim(self.UI_WIN, text=f"You are the Trustor.\nPress '1' to keep ${self.trustor_money}\nPress '3' to give ${self.trustor_money * 3}",
                                        pos=(0, 0), height=30, color='white')
        decision_text.draw()
        self.UI_WIN.flip()

        keys = event.waitKeys(keyList=['1', '3', 'escape'])

        if 'escape' in keys:
            core.quit()
        elif '1' in keys:
            self.decision = 'keep'
        elif '3' in keys:
            self.decision = 'give'

        return self.decision

    def trustee_decision(self):
        """
        Trustee's decision on whether to keep or share the money.
        """
        waiting_text = visual.TextStim(self.UI_WIN, text="You are the Trustee.\nWaiting for the Trustor's decision...",
                                       pos=(0, 0), height=30, color='white')
        waiting_text.draw()
        self.UI_WIN.flip()

        core.wait(random.uniform(0.5, 2))  # Random wait between 0.5 to 2 seconds

        if self.decision == 'give':
            received_amount = self.trustor_money * 3  # Trustee receives 3X what was given
            self.trustee_money += received_amount  # Add to trustee's total money
            returned_amount = self.cpu.decide_return(received_amount)  # Trustee decides how much to share back
            self.trustor_money = returned_amount  # Trustor receives the returned amount
            self.trustee_money -= returned_amount  # Deduct from trustee's money
            return returned_amount
        return 0  # If trustor kept the money, trustee gets nothing

    def outcome_phase(self):
        """
        Display the outcome and update the amounts for the next round.
        """
        if self.role == 'trustor':
            if self.decision == 'keep':
                outcome_text = visual.TextStim(self.UI_WIN, text=f"You kept ${self.trustor_money}.", pos=(0, 0), height=30, color='green')
                self.trustor_money = 1  # Trustor gets only $1 next round if they kept the money
            elif self.decision == 'give':
                returned_amount = self.trustee_decision()
                if returned_amount == 0:
                    outcome_text = visual.TextStim(self.UI_WIN, text="The trustee kept all the money.", pos=(0, 0), height=30, color='red')
                    self.trustor_money = 1  # Trustor gets only $1 next round if the trustee keeps everything
                else:
                    outcome_text = visual.TextStim(self.UI_WIN, text=f"The trustee returned ${returned_amount} to you.", pos=(0, 0), height=30, color='green')
                    # Trustor's money is already updated in trustee_decision()
        else:
            received_amount = self.trustor_money * 3  # What the trustee received from the trustor
            if self.cpu.keep_money(received_amount):
                outcome_text = visual.TextStim(self.UI_WIN, text=f"The Trustee kept ${received_amount}.", pos=(0, 0), height=30, color='red')
            else:
                returned_amount = self.cpu.decide_return(received_amount)
                outcome_text = visual.TextStim(self.UI_WIN, text=f"The Trustee returned ${returned_amount}.", pos=(0, 0), height=30, color='green')
                self.trustee_money -= returned_amount  # Update trustee's money after sharing
                self.trustor_money = returned_amount  # Trustor receives what was shared

        outcome_text.draw()
        self.UI_WIN.flip()

        core.wait(random.uniform(0.5, 2))  # Random wait between 0.5 to 2 seconds

