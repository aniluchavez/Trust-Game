# globals.py
from psychopy import core, prefs
import os
from parameters import Parameters 

# --- Set hardware preferences ---
prefs.hardware['audioLib'] = ['sounddevice', 'pygame']
prefs.hardware['audioLatencyMode'] = '3'
PARAMETERS=Parameters()
# --- Experiment Settings ---
EXPERIMENT_NAME = "Trust Game Experiment"
DATA_PATH = os.path.join(os.getcwd(), "data")  # Path to save data files

# Ensure data path exists
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

# --- Global Experiment Clock ---
ABS_CLOCK = core.Clock()  # Absolute clock to time the experiment phases

# --- Event Marking Variables ---
# Set event markers for start, stop, and specific phase transitions
EVENT_MARKERS = {
    "taskStart": "Task Started",
    "taskStop": "Task Ended Successfully",
    "taskAbort": "Task Aborted",
    "introStart": "Intro Started",
    "introEnd": "Intro Ended"
}

# --- Default UI Settings (for consistency) ---
UI_SETTINGS = {
    "bgColor": [-1, -1, -1],  # Black background
    "textColor": [1, 1, 1],   # White text
    "font": "Arial",
    "fontSize": 24
}

# --- Audio Settings ---
# Add any shared audio settings or resources here if needed
AUDIO_SETTINGS = {
    "sample_rate": 44100,
    "volume": 0.8
}

# --- Utility Functions ---
def reset_clock():
    """Reset the global absolute clock for timing consistency."""
    ABS_CLOCK.reset()
