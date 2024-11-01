import random
import globals as glb

class CPU:
    __slots__ = ('trustworthiness', 'weights', 'money')
    
    def __init__(self, trustworthiness='trustworthy', weights=None, initial_money=1):
        """
        Initialize CPU with specific trustworthiness and weights.

        Parameters:
        ----------
        trustworthiness : str
            Trustworthiness level ('trustworthy', 'untrustworthy', or 'neutral').
        weights : dict
            Weights dict defining the probability of sampling from high or low return ranges.
        initial_money : int
            Starting amount for the CPU partner.
        """
        self.trustworthiness = trustworthiness
        self.weights = weights if weights else (
            glb.PARAMETERS.trustworthy_weights if trustworthiness == 'trustworthy' 
            else glb.PARAMETERS.untrustworthy_weights if trustworthiness == 'untrustworthy' 
            else None  # Neutral has no specific weights
        )
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
        if self.trustworthiness == 'neutral':
            # Neutral randomly returns any value from 0 to 100% of the investment
            chosen_range = random.uniform(0.0, 1.0)
        else:
            # Trustworthy or untrustworthy CPU biased sampling
            if random.random() < self.weights['high']:
                chosen_range = random.uniform(0.5, 1.0)  # Higher return range
            else:
                chosen_range = random.uniform(0.0, 0.5)  # Lower return range
        return int(tripled_investment * chosen_range)


class GameLogic:
    def __init__(self, cpu_configs, initial_money=10, user_role="trustor"):
        self.initial_money = initial_money
        self.user_role = user_role
        self.trustor_balances = {i: initial_money for i in range(len(cpu_configs))}
        self.partner_returns = {i: 0 for i in range(len(cpu_configs))}  # Running total for each partner's returns
        self.cpus = [
            CPU(config['trustworthiness'], config.get('weights'), initial_money)
            for config in cpu_configs
        ]

    def get_fresh_pot(self):
        """Return a fresh pot amount between $1 and $5 for each trial."""
        return random.randint(1, 5)

    def trustor_decision(self, choice, cpu_index):
        fresh_pot = self.get_fresh_pot()
        
        if choice == 'invest':
            tripled_investment = fresh_pot * 3
            return tripled_investment
        elif choice == 'keep':
            return fresh_pot  # Amount kept by the user

    def outcome_phase(self, tripled_investment, cpu_index):
        """
        CPU partner decides the amount to return based on the trustor's investment.

        Parameters:
        ----------
        tripled_investment : int
            Tripled amount from the trustor's investment.
        cpu_index : int
            Index of the CPU partner for this trial.

        Returns:
        --------
        int
            Amount returned by the CPU.
        """
        returned_amount = 0
        if tripled_investment > 0:
            cpu = self.cpus[cpu_index]
            returned_amount = cpu.decide_return(tripled_investment)
            
            # Add to the cumulative return for this partner
            self.partner_returns[cpu_index] += returned_amount
            
            # Debug statement to confirm accurate tracking
            print(f"Trial with Partner {cpu_index} - Tripled Investment: {tripled_investment}, Returned: {returned_amount}, "
                  f"Running Total for Partner {cpu_index}: {self.partner_returns[cpu_index]}")
        return returned_amount
