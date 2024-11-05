import random
import globals as glb

class CPU:
    __slots__ = ('trustworthiness', 'weights', 'money')
    
    def __init__(self, trustworthiness='trustworthy', weights=None, initial_money=1):
        self.trustworthiness = trustworthiness
        self.weights = weights if weights else (
            glb.PARAMETERS.trustworthy_weights if trustworthiness == 'trustworthy' 
            else glb.PARAMETERS.untrustworthy_weights if trustworthiness == 'untrustworthy' 
            else None  # Neutral has no specific weights
        )
        self.money = initial_money  # Initial money for tracking purposes

    def decide_return(self, tripled_investment):
        if self.trustworthiness == 'neutral':
            chosen_range = random.uniform(0.0, 1.0)
        else:
            chosen_range = random.uniform(0.5, 1.0) if random.random() < self.weights['high'] else random.uniform(0.0, 0.5)
        return int(tripled_investment * chosen_range)


class GameLogic:
    def __init__(self, cpu_configs, initial_money=1, user_role="trustor"):
        self.initial_money = initial_money
        self.user_role = user_role
        self.trustor_balances = {i: 0 for i in range(len(cpu_configs))}  # Track cumulative gains per partner
        self.cumulative_returns = {i: 0 for i in range(len(cpu_configs))}  # Track returns per block per partner
        self.cpus = [CPU(config['trustworthiness'], config.get('weights'), initial_money) for config in cpu_configs]
        self.current_fresh_pot = None  # Fixed fresh pot for the current trial

    def set_fresh_pot(self):
        """Set a fresh pot amount for the current trial."""
        self.current_fresh_pot = random.randint(1, 5)

    def trustor_decision(self, choice, cpu_index):
        if self.current_fresh_pot is None:
            self.set_fresh_pot()  # Set if not already set
        
        if choice == 'invest':
            return self.current_fresh_pot * 3  # 3X investment if invested
        elif choice == 'keep':
            return self.current_fresh_pot  # Keep only the fresh pot

    def outcome_phase(self, tripled_investment, cpu_index):
        """Simulate the outcome phase and record the returned amount."""
        returned_amount = 0
        if tripled_investment > 0:
            cpu = self.cpus[cpu_index]
            returned_amount = cpu.decide_return(tripled_investment)
            self.trustor_balances[cpu_index] += returned_amount  # Track overall gains per partner
            self.cumulative_returns[cpu_index] += returned_amount  # Track cumulative returns for current block
            
            print(f"Trial with Partner {cpu_index} - Tripled Investment: {tripled_investment}, Returned: {returned_amount}, "
                  f"Total Gains from Partner {cpu_index}: {self.trustor_balances[cpu_index]}")
        
        return returned_amount

    def get_cumulative_returns(self):
        """Return cumulative amounts returned by each partner for the current block."""
        return self.cumulative_returns

    def reset_cumulative_returns(self):
        """Reset cumulative returns for a new block."""
        self.cumulative_returns = {index: 0 for index in self.cumulative_returns}
