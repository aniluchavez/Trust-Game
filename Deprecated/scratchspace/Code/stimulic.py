from psychopy import visual

# Create visual stimuli
def create_stimuli(UI_WIN, PARAMETERS):
    global UI_TEXT
    UI_TEXT = visual.TextStim(UI_WIN, text='Welcome', font=PARAMETERS.text['font'],
                              color=PARAMETERS.text['color'], height=PARAMETERS.text['size'])
    return UI_TEXT
