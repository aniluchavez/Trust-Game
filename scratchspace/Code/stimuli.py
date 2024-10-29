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
    return visual.ImageStim(
        UI_WIN,
        image=chosen_image,
        units="norm",  # Normalized units for consistent size on different screens
        pos=(0, 0.5),  # Position image towards the top
        size=(0.8, 0.8)  # Make image a bit smaller to fit comfortably
    )

def create_text_stimuli(UI_WIN, PARAMETERS, text_content, pos=(0, 0)):
    """
    Creates a TextStim object for displaying text.
    """
    try:
        return visual.TextStim(
            win=UI_WIN,
            text=text_content,
            font=PARAMETERS.text.get('font', 'Arial'),  # Default to Arial if unspecified
            color=PARAMETERS.text.get('color', [1, 1, 1]),  # Ensure color is in RGB format
            colorSpace='rgb',
            height=0.1,  # Default text height, should scale to 'norm' units
            units='norm',
            pos=pos
        )
    except Exception as e:
        print(f"Error creating TextStim for '{text_content}': {e}")
        return None


def create_button(UI_WIN, label, pos):
    """
    Creates a button with a rectangle background and text overlay.
    """
    button_rect = visual.Rect(
        win=UI_WIN,
        width=0.6,
        height=0.2,
        pos=pos,
        fillColor='blue',
        lineColor='blue'
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
    Creates a slider to rate trustworthiness on a scale of 1 to 10.
    """
    trust_slider=visual.Slider(
        win=UI_WIN,
        size=(0.8, 0.1),
        pos=(0, -0.7),
        labels=[str(i) for i in range(1, 11)],  # Scale labels from 1 to 10
        ticks=list(range(1, 11)),  # Ticks from 1 to 10
        granularity=1,
        style=['rating', 'triangleMarker'],
        labelHeight=0.04  # Adjust label font size for spacing
    )

    # Instruction text above the slider
    instructions_text = visual.TextStim(
        win=UI_WIN,
        text="Please rate the trustworthiness of your partner on the scale below. Move slider to desired ranking and press ENTER",
        pos=(0, -0.3),  # Position above the slider
        height=0.07
    )

    # Add text labels for "Not Trustworthy," "Neutral," and "Trustworthy"
    not_trustworthy_label =visual.TextStim(
        win=UI_WIN,
        text="Not Trustworthy",
        pos=(-0.4, -0.6),  # Position to the left of the slider
        height=0.05
    )
    
    neutral_label = visual.TextStim(
        win=UI_WIN,
        text="Neutral",
        pos=(0, -0.6),  # Position centered under the slider
        height=0.05
    )
    
    trustworthy_label = visual.TextStim(
        win=UI_WIN,
        text="Trustworthy",
        pos=(0.4, -0.6),  # Position to the right of the slider
        height=0.05
    )
    # Return the slider, instructions, and labels as a tuple
    return trust_slider, instructions_text, not_trustworthy_label, neutral_label, trustworthy_label
