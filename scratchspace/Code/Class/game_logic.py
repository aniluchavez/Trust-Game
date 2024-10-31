import random
import globals as glb


class CPU:
    __slots__ = ('trustworthiness', 'weights', 'money')
    def __init__(self, trustworthiness='trustworthy', weights=None, initial_money=1):
        """
        Initialize CPU with specific trustworthiness and weights.

        Parameters:
        ----------
        PARAMETERS : Parameters
            Object containing experiment-wide settings.
        trustworthiness : str
            Trustworthiness level ('trustworthy' or 'untrustworthy').
        weights : dict
            Weights dict defining the probability of sampling from high or low return ranges.
        initial_money : int
            Starting amount for the CPU partner.
        """
        self.trustworthiness = trustworthiness
        self.weights = weights if weights else glb.PARAMETERS.trustworthy_weights if trustworthiness == 'trustworthy' else glb.PARAMETERS.untrustworthy_weights
        self.money = initial_money  # Start money for this partner

    def decide_return(self, tripled_investment):
        """
        Decide how much to return based on trustworthiness and biased sampling.

        Parameters:
        ----------
        tripled_investment : int
            Tripled investment received from the trustor.

        Returns:
        --------
        int
            Amount the CPU decides to return to the trustor.
        """
        if random.random() < self.weights['high']:
            chosen_range = random.uniform(0.5, 1.0)  # Higher return range for trustworthy
        else:
            chosen_range = random.uniform(0.0, 0.5)  # Lower return range for untrustworthy
        return int(tripled_investment * chosen_range)

class GameLogic:
    def __init__(self, cpu_configs, initial_money=10, user_role="trustor"):
        """
        Initialize game logic with multiple CPU partners.

        Parameters:
        ----------
        PARAMETERS : Parameters
            Experiment settings and configurations.
        cpu_configs : list of dicts
            List containing configurations for each CPU partner.
        initial_money : int
            Starting amount for the trustor and each CPU.
        user_role : str
            Role of the user in the game ('trustor' or 'trustee').
        """
        self.initial_money = initial_money  # Define the starting amount for replenishment
        self.user_role = user_role  # Track user role (trustor or trustee)
        
        # Track each partner's balance separately for the trustor
        self.trustor_balances = {i: initial_money for i in range(len(cpu_configs))}
        
        # Create CPU partners
        self.cpus = [
            CPU(config['trustworthiness'], config.get('weights'), initial_money)
            for config in cpu_configs
        ]

    def reset_amounts(self):
        """Reset trustor money and all CPU balances at the start of each block."""
        for cpu_index in self.trustor_balances:
            self.trustor_balances[cpu_index] = self.initial_money  # Reset trustor's balance for each partner
        for cpu in self.cpus:
            cpu.money = self.initial_money  # Reset each CPU partner's balance

    def trustor_decision(self, choice, cpu_index):
        """
        Process the trustor's decision to keep or invest with a specific partner.

        Parameters:
        ----------
        choice : str
            Trustor's decision ('keep' or 'invest').
        cpu_index : int
            Index of the CPU partner for this trial.

        Returns:
        --------
        int
            Amount relevant to the outcome phase display.
        """
        current_balance = self.trustor_balances[cpu_index]
        
        if choice == 'invest':
            tripled_investment = current_balance * 3  # Only CPU's return will alter the balance
            return tripled_investment
        elif choice == 'keep':
            # Increase the balance by 1 if keeping the amount
            self.trustor_balances[cpu_index] += 1
            return current_balance  # Show the starting/accumulated amount, not tripled

    def outcome_phase(self, tripled_investment, cpu_index):
        """
        CPU partner decides the amount to return based on the trustor's investment.

        Parameters:
        ----------
        tripled_investment : int
            Tripled amount from the trustor's investment.
        cpu_index : int
            Index to select the correct CPU partner for this trial.

        Returns:
        --------
        int
            Amount returned by the CPU.
        """
        if tripled_investment > 0:
            cpu = self.cpus[cpu_index]
            returned_amount = cpu.decide_return(tripled_investment)
            
            # Add the returned amount to the trustor's balance for this specific partner
            previous_balance = self.trustor_balances[cpu_index]
            self.trustor_balances[cpu_index] += returned_amount
            new_balance = self.trustor_balances[cpu_index]
            
            # Debug statement to confirm accurate balance
            print(f"Trial with Partner {cpu_index} - Tripled Investment: {tripled_investment}, Returned: {returned_amount}, "
                  f"Previous Balance: {previous_balance}, New Balance: {new_balance}")
        else:
            returned_amount = 0

        # Ensure at least the starting amount in trustor's balance for the next round with this partner
        if self.trustor_balances[cpu_index] < self.initial_money:
            self.trustor_balances[cpu_index] = self.initial_money

        return returned_amount

# import random

# class CPU:
#     def __init__(self, PARAMETERS, trustworthiness='trustworthy', weights=None, initial_money=1):
#         self.trustworthiness = trustworthiness
#         self.weights = weights if weights else PARAMETERS.trustworthy_weights if trustworthiness == 'trustworthy' else PARAMETERS.untrustworthy_weights
#         self.money = initial_money  # Start money for this partner

#     def decide_return(self, received_amount):
#         # Sample a biased proportion to return based on weights
#         if random.random() < self.weights['high']:
#             chosen_range = random.uniform(0.5, 1.0)  # Higher return range for trustworthy
#         else:
#             chosen_range = random.uniform(0.0, 0.5)  # Lower return range for untrustworthy
#         return int(received_amount * chosen_range)
    
# class GameLogic:
#     def __init__(self, PARAMETERS, cpu_configs, initial_money=1, user_role="trustor"):
#         """
#         Initialize game logic with multiple CPU partners.

#         Parameters:
#         ----------
#         PARAMETERS : Parameters
#             Experiment settings and configurations.
#         cpu_configs : list of dicts
#             List containing configurations for each CPU partner.
#         initial_money : int
#             Starting amount for the trustor and each CPU.
#         user_role : str
#             Role of the user in the game ('trustor' or 'trustee').
#         """
#         self.initial_money = initial_money
#         self.user_role = user_role  # Track user role (trustor or trustee)
        
#         # Track each partner's balance separately for the trustor
#         self.trustor_balances = {i: initial_money for i in range(len(cpu_configs))}
        
#         # Create CPU partners
#         self.cpus = [
#             CPU(PARAMETERS, config['trustworthiness'], config.get('weights'), initial_money)
#             for config in cpu_configs
#         ]

#     def reset_amounts(self):
#         """Reset trustor money and all CPU balances at the start of each block."""
#         for cpu_index in self.trustor_balances:
#             self.trustor_balances[cpu_index] = self.initial_money  # Reset trustor's balance for each partner
#         for cpu in self.cpus:
#             cpu.money = self.initial_money  # Reset each CPU partner's balance

#     def trustor_decision(self, choice, cpu_index):
#         """
#         Process the trustor's decision to keep or give for a specific partner.

#         Parameters:
#         ----------
#         choice : str
#             Trustor's decision ('keep' or 'give').
#         cpu_index : int
#             Index of the CPU partner for this trial.

#         Returns:
#         --------
#         int
#             Amount relevant to the outcome phase display.
#         """
#         if self.user_role == "trustor":
#             # Trustor is the user
#             if choice == 'give':
#                 amount_given = self.trustor_balances[cpu_index] * 3  # Calculate amount to give based on current balance
#                 self.trustor_balances[cpu_index] = 0  # Reset balance after giving
#                 return amount_given
#             elif choice == 'keep':
#                 current_amount = self.trustor_balances[cpu_index]  # Store current amount for display
#                 self.trustor_balances[cpu_index] += 1  # Increase balance by 1 for this specific partner
#                 return current_amount
#         else:
#             # Trustor is the CPU, and they make their own decision
#             cpu = self.cpus[cpu_index]
#             return cpu.decide_return(cpu.money)

#     def outcome_phase(self, amount_given, cpu_index):
#         """
#         CPU partner decides the amount to return based on the trustor's given amount.

#         Parameters:
#         ----------
#         amount_given : int
#             Amount given by the trustor.
#         cpu_index : int
#             Index to select the correct CPU partner for this trial.

#         Returns:
#         --------
#         int
#             Amount returned by the CPU.
#         """
#         if amount_given > 0:
#             # Get the specific CPU partner based on index
#             cpu = self.cpus[cpu_index]
#             cpu.money += amount_given  # Increase this CPU's balance by the given amount
#             returned_amount = cpu.decide_return(amount_given)
            
#             # Add the returned amount to the trustor's balance for this specific partner
#             self.trustor_balances[cpu_index] += returned_amount

#             # Debug statement to verify accumulation behavior
#             print(f"Trial with Partner {cpu_index} - Amount given: {amount_given}, Returned: {returned_amount}, "
#                   f"Previous Balance: {self.trustor_balances[cpu_index] - returned_amount}, "
#                   f"New Balance: {self.trustor_balances[cpu_index]}")
#         else:
#             returned_amount = 0

#         # Ensure at least $1 in trustor's balance for the next round with this partner
#         if self.trustor_balances[cpu_index] == 0:
#             self.trustor_balances[cpu_index] = 1

#         return returned_amount





