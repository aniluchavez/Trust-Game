import random

class CPU:
    def __init__(self, PARAMETERS, trustworthiness='trustworthy'):
        """
        Initialize CPU with trustworthiness level and weights from PARAMETERS.

        Parameters:
        ----------
        PARAMETERS : Parameters
            Object containing experiment-wide settings.
        trustworthiness : str
            'trustworthy' or 'untrustworthy', determines CPU's behavior.
        """
        self.trustworthiness = trustworthiness
        self.weights = PARAMETERS.trustworthy_weights if trustworthiness == 'trustworthy' else PARAMETERS.untrustworthy_weights

    def decide_return(self, received_amount):
        """
        Decide amount to return based on trustworthiness and weights.

        Parameters:
        ----------
        received_amount : int
            The amount the CPU received from the trustor.

        Returns:
        --------
        int
            Amount the CPU decides to return.
        """
        low_range = random.uniform(0.0, 0.6)
        high_range = random.uniform(0.6, 0.9)
        chosen_range = low_range if random.random() < self.weights['low'] else high_range
        return int(received_amount * chosen_range)

class GameLogic:
    def __init__(self, PARAMETERS, trustworthiness='trustworthy', initial_money=1):
        """
        Initialize game logic with a CPU and initial money.

        Parameters:
        ----------
        PARAMETERS : Parameters
            Object with settings for the experiment.
        trustworthiness : str
            Trustworthiness of the CPU ('trustworthy' or 'untrustworthy').
        initial_money : int
            Starting money for the trustor.
        """
        self.trustor_money = initial_money
        self.cpu = CPU(PARAMETERS, trustworthiness)

    def trustor_decision(self, choice):
        """
        Process the trustor's decision.

        Parameters:
        ----------
        choice : str
            Decision made by the trustor ('keep' or 'give').

        Returns:
        --------
        int
            Amount given if 'give', or 0 if 'keep'.
        """
        if choice == 'give':
            amount_given = self.trustor_money * 3
            self.trustor_money = 0  # Reset to 0, updated in outcome phase based on CPU return
            return amount_given
        elif choice == 'keep':
            self.trustor_money += 1  # Increment if keeping
            return 0
        else:
            raise ValueError("Invalid choice. Choose 'keep' or 'give'.")

    def outcome_phase(self, amount_given):
        """
        CPU decides the amount to return based on trustworthiness.

        Parameters:
        ----------
        amount_given : int
            Amount given by the trustor.

        Returns:
        --------
        int
            Amount returned by the CPU.
        """
        if amount_given > 0:
            returned_amount = self.cpu.decide_return(amount_given)
            self.trustor_money += returned_amount  # Update user's money with returned amount
            return returned_amount
        return 0
