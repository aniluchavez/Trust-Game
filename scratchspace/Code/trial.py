from psychopy import core, event
from stimuli import create_text_stimuli, create_button, create_trust_slider
from psychopy.visual import TextStim
import globals as glb
from markEvent import markEvent


def show_welcome():
    """Display welcome message and game instructions at the start of the experiment."""
    
    # Create the welcome text stimuli
    welcome_text = TextStim(
        win=glb.UI_WIN,
        text="Welcome to the Trust Game Experiment!\n\nIn this game, you'll be interacting with a partner that precorded their responses.\n\n "
             "You are the trustor and start with $1 in your account.\n"
             "You can choose to keep or give money, and your partner may choose to share some amount back or keep it all for themselves.\n\n"
             "Press 'Enter' to continue.",
        pos=(0, 0),  # Center of the screen
        height=0.09,  # Adjust text size as needed
        wrapWidth=1.5  # Wrap the text for readability
    )
    # Draw and wait for participant to press Enter
    response = None
    while response is None:
        welcome_text.draw()
        glb.UI_WIN.flip()
        # Wait for Enter key to confirm
        keys = event.getKeys(keyList=['return'])
        if 'return' in keys:
            response = True  # Exit the loop once Enter is pressed
    # Briefly display a message to confirm the start of the experiment
    confirmation_text = TextStim(
        win=glb.UI_WIN,
        text="Let's begin!",
        pos=(0, -0.5),
        height=0.1
    )
    for _ in range(30):  # Display for ~1 second
        confirmation_text.draw()
        glb.UI_WIN.flip()
    
    # Clear the screen before proceeding
    glb.UI_WIN.flip()


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
        self.intro_displayed = False  # Flag to control intro display
        self.setup_stimuli()

    def setup_stimuli(self):
        """Initialize and set up visual components for the trial."""
        # Initialize partner name text
        if not hasattr(self, 'partner_name_text'):
            self.partner_name_text = create_text_stimuli(
                self.UI_WIN, self.PARAMETERS, f"Partner: {self.partner_name}", pos=(0, 0)
            )
        # Initialize trust slider and labels
        if not hasattr(self, 'trust_slider'):
            self.trust_slider, self.instructions_text, self.not_trustworthy_label, \
            self.neutral_label, self.trustworthy_label = create_trust_slider(self.UI_WIN)
        # Initialize response recorded text, this position is perfect!
        if not hasattr(self, 'response_recorded_text'):
            self.response_recorded_text = create_text_stimuli(
                self.UI_WIN, self.PARAMETERS, "Response recorded", pos=(0, -0.9)
            )
        # Only create buttons if game_logic is provided
        if self.game_logic is not None:
            if not hasattr(self, 'keep_button_rect'):
                self.keep_button_rect, self.keep_button_text = create_button(
                    self.UI_WIN, label=f"Keep ${self.game_logic.trustor_money}", pos=(-0.4, -0.5)
                )       
            if not hasattr(self, 'give_button_rect'):
                self.give_button_rect, self.give_button_text = create_button(
                    self.UI_WIN, label=f"Give ${self.game_logic.trustor_money * 3}", pos=(0.4, -0.5)
                )
        # Initialize outcome text
        if not hasattr(self, 'outcome_text'):
            self.outcome_text = create_text_stimuli(self.UI_WIN, self.PARAMETERS, text_content="", pos=(0, 0))

    def show_welcome(self):
        """Display welcome message and game instructions at the start of the experiment."""
        
        # Create the welcome text stimuli
        welcome_text = TextStim(
            win=self.UI_WIN,
            text="Welcome to the Trust Game Experiment!\n\nIn this game, you'll be interacting with a partner that precorded their responses.\n\n "
                 "You are the trustor and start with $1 in your account.\n"
                 "You can choose to keep or give money, and your partner may choose to share some amount back or keep it all for themselves.\n\n"
                 "Press 'Enter' to continue.",
            pos=(0, 0),  # Center of the screen
            height=0.09,  # Adjust text size as needed
            wrapWidth=1.5  # Wrap the text for readability
        )

        # Draw and wait for participant to press Enter
        response = None
        while response is None:
            welcome_text.draw()
            self.UI_WIN.flip()

            # Wait for Enter key to confirm
            keys = event.getKeys(keyList=['return'])
            if 'return' in keys:
                response = True  # Exit the loop once Enter is pressed

        # Briefly display a message to confirm the start of the experiment
        confirmation_text = TextStim(
            win=self.UI_WIN,
            text="Let's begin!",
            pos=(0, -0.5),
            height=0.1
        )
        for _ in range(30):  # Display for ~1 second
            confirmation_text.draw()
            self.UI_WIN.flip()
        
        # Clear the screen before proceeding
        self.UI_WIN.flip()

    def show_intro(self):
        """Display introductory screen with partner's name, image, trust slider, and labels, allowing Enter key to confirm."""
        if self.intro_displayed:
            return
        self.intro_displayed = True

        # Unpack the slider and labels
        self.trust_slider, self.instructions_text, self.not_trustworthy_label, \
        self.neutral_label, self.trustworthy_label = create_trust_slider(self.UI_WIN)

        self.trust_slider.reset()  # Reset slider to default position
        response = None

        while response is None:
            # Draw intro elements
            self.partner_image.draw()
            self.partner_name_text.draw()
            self.instructions_text.draw()
            self.trust_slider.draw()
            self.not_trustworthy_label.draw()
            self.neutral_label.draw()
            self.trustworthy_label.draw()
            self.UI_WIN.flip()

            # Wait for Enter key to confirm the slider position
            keys = event.getKeys(keyList=['return'])
            if 'return' in keys:
                response = self.trust_slider.getRating() or 5  # Default to 5 if not moved
                markEvent("IntroSlider", rating=response, time=glb.ABS_CLOCK.getTime())

        # Briefly display "Response recorded" text
        for _ in range(30):  # Display for ~1 second
            self.partner_image.draw()
            self.partner_name_text.draw()
            self.trust_slider.draw()
            self.not_trustworthy_label.draw()
            self.neutral_label.draw()
            self.trustworthy_label.draw()
            self.response_recorded_text.draw()
            self.UI_WIN.flip()

        return response
    # Decision and outcome phases... Basically rendering the brunt of the experiment
    
    def run_decision_phase(self):
        """Decision phase where the user chooses to keep or give."""
        # Update button text with current amounts
        self.keep_button_text.text = f"Keep ${self.game_logic.trustor_money}"
        self.give_button_text.text = f"Give ${self.game_logic.trustor_money * 3}"

        # Draw decision phase elements
        self.partner_image.draw()
        self.partner_name_text.draw()
        self.keep_button_rect.draw()
        self.keep_button_text.draw()
        self.give_button_rect.draw()
        self.give_button_text.draw()
        self.UI_WIN.flip()

        # Get user input
        keys = event.waitKeys(keyList=['1', '3', 'escape'])
        if 'escape' in keys:
            core.quit()
        decision = 'keep' if '1' in keys else 'give'
        
        # Process the decision and get the amount for display
        amount_given = self.game_logic.trustor_decision(decision)

        return {"choice": decision, "amount": amount_given}

    def run_outcome_phase(self, decision_data):
        """Outcome phase where results are displayed based on the user's decision and CPU response."""
        decision = decision_data["choice"]
        amount_given = decision_data["amount"]

        # Determine outcome based on the decision
        if decision == "keep":
            outcome_message = f"You kept ${amount_given}"  # Display the amount before increment
        else:
            # CPU processes the return if the trustor decided to give
            returned_amount = self.game_logic.outcome_phase(amount_given)
            if returned_amount > 0:
                outcome_message = f"Partner returned ${returned_amount}"
            else:
                outcome_message = "Partner kept the money"
                # Check if the user's balance was replenished to $1
                if self.game_logic.trustor_money == 1:
                    outcome_message += " (Your balance was replenished to $1)"

        # Display the outcome message
        self.outcome_text.text = outcome_message
        self.outcome_text.draw()
        self.UI_WIN.flip()
        core.wait(1)  # Display outcome for 2 seconds

        # Return final outcome data
        return {
            "choice": decision,
            "amount_given": amount_given if decision == "give" else 0,
            "amount_returned": returned_amount if decision == "give" else 0
        }



    # This is the end of block ranking
    def show_block_ranking(self):
        """Display trustworthiness ranking screen at the end of the block, allowing Enter key to confirm."""
        # Reset the slider and capture the rating
        self.trust_slider.reset()  # Reset slider to default position
        response = None

        while response is None:
            # Draw ranking elements
            self.partner_image.draw()
            self.partner_name_text.draw()
            self.instructions_text.draw()
            self.trust_slider.draw()
            self.not_trustworthy_label.draw()
            self.neutral_label.draw()
            self.trustworthy_label.draw()
            self.UI_WIN.flip()

            # Wait for Enter key to confirm the slider position
            keys = event.getKeys(keyList=['return'])
            if 'return' in keys:
                response = self.trust_slider.getRating() or 5  # Default to 5 if not moved
                markEvent("BlockEndRanking", rating=response, time=glb.ABS_CLOCK.getTime())

        # Briefly display "Rating recorded" text
        for _ in range(30):  # Display for ~1 second
            self.partner_image.draw()
            self.partner_name_text.draw()
            self.trust_slider.draw()
            self.not_trustworthy_label.draw()
            self.neutral_label.draw()
            self.trustworthy_label.draw()
            self.response_recorded_text.draw()
            self.UI_WIN.flip()

        return response  # Return the end-of-block rating

    def run_trial(self):
        """Run welcome, intro, decision, and outcome phases and return trial data."""
        glb.reset_clock()
        markEvent("trialStart", trialIdx=self.trialIdx, blockIdx=self.blockIdx)

        # Only show intro if it's the first trial in the block and intro hasn't been shown
        if self.trialIdx == 0 and not self.intro_displayed:
            self.show_intro()  # Will set intro_displayed to True

        # Proceed with decision and outcome phases
        user_decision = self.run_decision_phase()
        decision_time = glb.ABS_CLOCK.getTime()
        markEvent("UserChoice", role=self.user_role, decision=user_decision["choice"], time=decision_time)

        # Outcome Phase
        cpu_response = self.run_outcome_phase(user_decision)  # Pass the entire decision dictionary
        outcome_time = glb.ABS_CLOCK.getTime()
        markEvent("OutcomeEnd", returned_amount=cpu_response["amount_returned"], time=outcome_time)

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
