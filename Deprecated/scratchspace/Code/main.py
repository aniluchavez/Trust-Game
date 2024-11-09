from distutils import core
from globals import create_globals, showExpInfoDlg
from stimuli import create_general_stimuli

def run_experiment():
    # Initialize global variables and clocks
    create_globals()
    
    # Show participant info dialog
    expInfo = showExpInfoDlg()
    UI_WIN = create_globals()
    # Create all stimuli
    UI_TEXT = create_general_stimuli(UI_WIN)
    
    # Now the experiment can begin
    UI_TEXT.draw()  # Display text stimulus
    UI_WIN.flip()  # Refresh the window to display the stimulus

    core.wait(2)  # Wait for 2 seconds

if __name__ == '__main__':
    run_experiment()

