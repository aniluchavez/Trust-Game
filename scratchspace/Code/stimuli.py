from psychopy import visual
import os
import random

def load_partner_image(UI_WIN, folder_path):
    """
    Load a random image from the folder and create an ImageStim.

    Parameters:
    ----------
    UI_WIN : psychopy.visual.Window
        The PsychoPy window where the image will be displayed.
    folder_path : str
        Path to the folder containing image files.

    Returns:
    --------
    visual.ImageStim
        Image stimulus with the chosen image file.
    """
    # Select a random image from the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    if not image_files:
        raise FileNotFoundError(f"No .jpg images found in directory {folder_path}")
    chosen_image = os.path.join(folder_path, random.choice(image_files))
    print(f"Chosen image for partner: {chosen_image}")  # Debugging print statement
    return visual.ImageStim(UI_WIN, image=chosen_image, pos=(0, 0.5), size=(0.5, 0.5))
from psychopy import visual

def create_text_stimuli(UI_WIN, PARAMETERS, text_content, pos=(0, 0)):
    """
    Creates a TextStim object.

    Parameters:
    ----------
    UI_WIN : psychopy.visual.Window
        The PsychoPy window object.
    PARAMETERS : Parameters
        Object containing experiment-wide settings.
    text_content : str
        Text to display.
    pos : tuple
        Position of the text on the screen.

    Returns:
    --------
    TextStim
        TextStim object ready to be drawn on the screen.
    """
    return visual.TextStim(
        win=UI_WIN,
        text=text_content,
        font=PARAMETERS.text['font'],
        color=PARAMETERS.text['color'],
        height=PARAMETERS.text['size'],
        pos=pos
    )

def create_button(UI_WIN, label, pos):
    """
    Creates a button with a background rectangle and text overlay.

    Parameters:
    ----------
    UI_WIN : psychopy.visual.Window
        The PsychoPy window object.
    label : str
        Label of the button.
    pos : tuple
        Position of the button on the screen.

    Returns:
    --------
    tuple
        A tuple containing the rectangle background and text overlay.
    """
    # Background rectangle for the button
    button_rect = visual.Rect(
        win=UI_WIN,
        width=0.3,
        height=0.15,
        pos=pos,
        fillColor='blue',
        lineColor='white'
    )
    # Text overlay for the button
    button_text = visual.TextStim(
        win=UI_WIN,
        text=label,
        pos=pos,
        height=0.08,
        color='white'
    )
    return button_rect, button_text


