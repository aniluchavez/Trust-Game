from psychopy import visual
import os
import random

# Create text stimuli
def create_text_stimuli(UI_WIN, PARAMETERS, text_content):
    """
    Create a flexible text stimulus that takes dynamic input.
    Parameters:
    ----------
    UI_WIN : psychopy.visual.Window
        The PsychoPy window object.
    PARAMETERS : dict
        A dictionary containing text properties like font, color, and size.
    text_content : str
        The dynamic text to be displayed.
    Returns:
    --------
    visual.TextStim
        A PsychoPy TextStim object with the specified dynamic text.
    """
    UI_TEXT = visual.TextStim(
        UI_WIN, 
        text=text_content,  # Dynamic text content
        font=PARAMETERS['text']['font'],
        color=PARAMETERS['text']['color'], 
        height=PARAMETERS['text']['size']
    )
    return UI_TEXT

def load_images_from_folder(folder_path,num_images):
    """
    Load and randomly select a set number of images from a folder.
    
    Parameters:
    ----------
    folder_path : str
        Path to the folder containing image files.
    num_images : int
        Number of images to randomly select.
        
    Returns:
    --------
    list
        A list of randomly selected image file paths.
    """
    all_images=[f for f in os.listdir(folder_path) if f.endswith ('.jpg')]

    if len(all_images)< num_images:
        raise ValueError("Not enough images in the folder to select the requested number of images")
    
    selected_images=random.sample(all_images,num_images)
    
    selected_image_paths = [os.path.join(folder_path, img) for img in selected_images]

    return selected_image_paths

def create_image_stimuli(UI_WIN, image_paths):
    """
    Create PsychoPy ImageStim objects for each image.
    
    Parameters:
    ----------
    UI_WIN : psychopy.visual.Window
        The PsychoPy window object to display stimuli.
    image_paths : list
        List of file paths to images.
        
    Returns:
    --------
    list
        A list of PsychoPy ImageStim objects.
    """
    image_stimuli = []
    
    for img_path in image_paths:
        # Create an ImageStim for each image
        stim = visual.ImageStim(UI_WIN, image=img_path, pos=(0, 0.6), size=(512, 512))  # Adjust size/position as needed
        image_stimuli.append(stim)
    
    return image_stimuli


def create_button_stim(UI_WIN, label, pos=(0, 0), size=(0.2, 0.1),):
    """
    Create a button stimulus with hover and click feedback.
    
    Parameters:
    ----------
    UI_WIN : psychopy.visual.Window
        The PsychoPy window object to display stimuli.
    label : str
        The text label for the button.
    pos : tuple
        The position of the button (default is center).
    size : tuple
        The size of the button (default is 0.2 width and 0.1 height in normalized units).
        
    Returns:
    --------
    visual.ButtonStim
        A PsychoPy ButtonStim object with the specified label.
    """
    
    button = visual.ButtonStim(
        win=UI_WIN,
        text=label,  # Set the button label dynamically
        pos=pos,  # Position of the button
        size=size,  # Size of the button
        color='white',  # Button border color
        fillColor='blue',  # Button fill color
        textColor='black',  # Text color
        hoverColor='green',  # Hover color
        clickColor='red'  # Color when the button is clicked
    )
    return button

def create_text_overlay_rect(UI_WIN, PARAMETERS, text):
    """
    Create a white rectangle with dynamic text overlay.
    
    Parameters:
    ----------
    UI_WIN : psychopy.visual.Window
        The PsychoPy window object to display stimuli.
    PARAMETERS : dict
        A dictionary containing text properties like font, color, and size.
    text : str
        The text to display over the white rectangle (can be a dynamic amount).
        
    Returns:
    --------
    tuple
        A tuple containing the rectangle (visual.Rect) and text (visual.TextStim) stimuli.
    """
    # Create the white rectangle
    rect = visual.Rect(
        UI_WIN,
        width=0.6,  # Width of rectangle in normalized units
        height=0.3,  # Height of rectangle in normalized units
        fillColor='white',  # White background
        pos=(0, 0.5)  # Position in the window
    )
    
    # Create the overlayed text with dynamic content
    overlay_text = visual.TextStim(
        UI_WIN,
        text=text,  # Dynamic text to display (e.g., amount)
        font=PARAMETERS['text']['font'],
        color=PARAMETERS['text']['color'],
        height=PARAMETERS['text']['size'],
        pos=(0, 0.5)  # Same position as the rectangle
    )
    
    return rect, overlay_text




def create_general_stimuli(UI_WIN, folder_path, num_images, PARAMETERS,button_labels,overlay_text):
    """
    Create both text and image stimuli and return them.
    
    Parameters:
    ----------
    UI_WIN : psychopy.visual.Window
        The PsychoPy window object to display stimuli.
    folder_path : str
        Path to the folder containing image files.
    num_images : int
        Number of images to randomly select.
    PARAMETERS : dict
        A dictionary containing text properties like font, color, and size.
        
    Returns:
    --------
    dict
        A dictionary containing both text and image stimuli.
    """
    from random import sample
    import os
    
    # Load and randomly select images from folder
    all_images = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    selected_images = sample(all_images, num_images)
    selected_image_paths = [os.path.join(folder_path, img) for img in selected_images]
    
    # Create text stimulus
    welcome_text_stim = create_text_stimuli(UI_WIN, PARAMETERS)
    rect, overlay_text_stim = create_text_overlay_rect(UI_WIN, PARAMETERS, overlay_text)
    
    # Create buttons with dynamic labels
    button1 = create_button_stim(UI_WIN, label=button_labels[0], pos=(-0.4, 0), size=(0.3, 0.15))
    button2 = create_button_stim(UI_WIN, label=button_labels[1], pos=(0, 0), size=(0.3, 0.15))
    # Create image stimuli
    image_stims = create_image_stimuli(UI_WIN, selected_image_paths)
    slider = visual.Slider(
        win=UI_WIN,
        size=(0.8, 0.1),  # Slider size
        pos=(0, -0.2),  # Slider position
        labels=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],  # Labels along the slider
        ticks=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Tick values
        style="slider",  # Slider style
        granularity=1,  # Allow only whole number responses
        color='black',  # Slider bar color
        fontSize=20,
    )
    # Return all stimuli
    return {
        'overlay_rect': rect,
        'welcome_text':welcome_text_stim,
        'overlay_text': overlay_text_stim,
        'buttons': [button1, button2],
        'slider': slider,
        'images': image_stims
    }
