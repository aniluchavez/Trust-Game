from psychopy import visual
import os
import random

def load_partner_image(UI_WIN, folder_path):
    """
    Load a random image from the folder and create an ImageStim.
    """
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    if not image_files:
        raise FileNotFoundError(f"No .jpg images found in directory {folder_path}")
    chosen_image = os.path.join(folder_path, random.choice(image_files))
    print(f"Chosen image for partner: {chosen_image}")
    return visual.ImageStim(UI_WIN, image=chosen_image, pos=(0, 0.5), size=(0.5, 0.5))

def create_text_stimuli(UI_WIN, PARAMETERS, text_content, pos=(0, 0)):
    """
    Creates a TextStim object for displaying text.
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
    Creates a button with a rectangle background and text overlay.
    """
    button_rect = visual.Rect(
        win=UI_WIN,
        width=0.3,
        height=0.15,
        pos=pos,
        fillColor='blue',
        lineColor='white'
    )
    button_text = visual.TextStim(
        win=UI_WIN,
        text=label,
        pos=pos,
        height=0.08,
        color='white'
    )
    return button_rect, button_text

def create_trust_slider(UI_WIN):
    """
    Creates a slider to rate trustworthiness.
    """
    return visual.Slider(
        win=UI_WIN, size=(0.8, 0.1), pos=(0, -0.4),
        labels=["Not Trustworthy", "Neutral", "Very Trustworthy"],
        ticks=[1, 2, 3, 4, 5, 6, 7],
        granularity=1
    )
