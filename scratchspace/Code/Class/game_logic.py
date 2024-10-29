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
        Decide amount to return based on trustworthiness and biased sampling.

        Parameters:
        ----------
        received_amount : int
            The amount the CPU received from the trustor.

        Returns:
        --------
        int
            Amount the CPU decides to return.
        """
        # Bias towards a specific range based on weights and trustworthiness
        if random.random() < self.weights['high']:
            # Higher probability of sampling from the higher range for trustworthy, lower for untrustworthy
            chosen_range = random.uniform(0.5, 1.0)
        else:
            # Lower probability range
            chosen_range = random.uniform(0.0, 0.5)

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
        self.cpu_money = initial_money  # Initialize CPU's starting money
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
            Amount relevant to the outcome display.
        """
        if choice == 'give':
            amount_given = self.trustor_money * 3
            self.trustor_money = 0  # Reset to 0 after giving; will be updated in outcome phase
            return amount_given
        elif choice == 'keep':
            initial_money = self.trustor_money  # Store amount before increase for display
            self.trustor_money += 1  # Increase by 1 if keeping
            return initial_money
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
            # CPU receives amount, update cpu_money based on received amount
            self.cpu_money += amount_given
            returned_amount = self.cpu.decide_return(amount_given)
            self.trustor_money += returned_amount  # Update trustor's money with the returned amount
        else:
            returned_amount = 0

        # Ensure the trustor has at least $1 for the next round
        if self.trustor_money == 0:
            self.trustor_money = 1

        return returned_amount
