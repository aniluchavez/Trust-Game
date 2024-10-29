import random
from psychopy import visual, event, core
import os

class LotteryTrial:
    def __init__(self, UI_WIN, PARAMETERS, image_folder="Images"):
        """
        Initialize the Lottery Trial with necessary components.

        Parameters:
        ----------
        UI_WIN : psychopy.visual.Window
            The PsychoPy window in which stimuli are displayed.
        PARAMETERS : Parameters
            Object containing experiment-wide settings.
        image_folder : str
            Path to the folder where images are stored.
        """
        self.UI_WIN = UI_WIN
        self.PARAMETERS = PARAMETERS
        self.image_folder = image_folder
        self.setup_stimuli()

    def setup_stimuli(self):
        """Set up visual stimuli for the lottery trial."""
        # Load slot machine image
        slot_machine_image_path = os.path.join(self.image_folder, "slot_machine.jpg")
        self.slot_machine_image = visual.ImageStim(self.UI_WIN, image=slot_machine_image_path)

        # Set up Yes and No buttons with instructions
        self.yes_button_text = visual.TextStim(self.UI_WIN, text="Press 1 to play", pos=(-0.3, -0.5))
        self.no_button_text = visual.TextStim(self.UI_WIN, text="Press 3 to skip", pos=(0.3, -0.5))

        # Text to display the outcome
        self.outcome_text = visual.TextStim(self.UI_WIN, text="", pos=(0, 0.2))

    def run_lottery_trial(self):
        """Run a single lottery trial where the user decides to play or not and sees the outcome."""
        # Display the slot machine and choice buttons
        self.slot_machine_image.draw()
        self.yes_button_text.draw()
        self.no_button_text.draw()
        self.UI_WIN.flip()

        # Wait for user input (1 for Yes or 3 for No)
        keys = event.waitKeys(keyList=['1', '3', 'escape'])
        if 'escape' in keys:
            core.quit()
        play_lottery = '1' in keys  # True if Yes (1), False if No (3)

        # Determine the lottery outcome with 50% chance of winning if the user chose to play
        if play_lottery:
            outcome = "win" if random.random() < 0.5 else "lose"
            self.outcome_text.text = "You won the lottery!" if outcome == "win" else "You lost the lottery."
        else:
            self.outcome_text.text = "You chose not to play."

        # Display the outcome
        self.outcome_text.draw()
        self.UI_WIN.flip()
        core.wait(2)  # Display outcome for 2 seconds

        # Return trial data
        return {
            "played": play_lottery,
            "outcome": outcome if play_lottery else "not_played"
        }
