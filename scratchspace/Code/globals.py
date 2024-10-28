from psychopy import core, prefs, visual
import os
from parameters import Parameters 

# Set hardware preferences
prefs.hardware['audioLib'] = ['sounddevice', 'pygame']
prefs.hardware['audioLatencyMode'] = '3'

# Load parameters globally
PARAMETERS = Parameters()

# Set up experiment settings
EXPERIMENT_NAME = "Trust Game Experiment"
DATA_PATH = os.path.join(os.getcwd(), "data")
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

# Global experiment clock
ABS_CLOCK = core.Clock()

# Global UI Window creation
UI_WIN = PARAMETERS.create_window()

# Utility function to reset the clock
def reset_clock():
    ABS_CLOCK.reset()


#removed stuff from eventmarkers because that is now handled by markEvents