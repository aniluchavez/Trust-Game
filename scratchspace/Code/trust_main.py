# from globals import create_globals, showExpInfoDlg
# from stimuli import create_stimuli

# def run_experiment():
#     # Initialize global variables and clocks
#     create_globals()
    
#     # Show participant info dialog
#     expInfo = showExpInfoDlg()
    
#     # Create all stimuli
#     #UI_TEXT = create_stimuli(UI_WIN, PARAMETERS)
    
#     # Now the experiment can begin
#     #UI_TEXT.draw()  # Display text stimulus
#    # UI_WIN.flip()  # Refresh the window to display the stimulus

#    # core.wait(2)  # Wait for 2 seconds

# if __name__ == '__main__':
#     run_experiment()

# trust_main.py
from experiment import run_experiment

if __name__ == "__main__":
    # Launch the experiment using the configuration specified in parameters.py
    run_experiment()
