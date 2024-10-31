from psychopy import visual
import os
import random
import globals as glb
import os
import random

TEXT_CONV = glb.PARAMETERS.window['size'][1]/2
# TEXT = visual.TextBox2(glb.UI_WIN, text="", font = glb.PARAMETERS.text['font'], letterHeight=glb.PARAMETERS.text['size']/TEXT_CONV, 
#                        colorSpace='rgb255', color=glb.PARAMETERS.text['color'], alignment='center', units='norm')
TEXT_TEXT = ''
TEXT_POS = (0,0)
TEXT_HEIGHT = glb.PARAMETERS.text['size']/TEXT_CONV
TEXT_COLOR = glb.PARAMETERS.text['color']
TEXT = visual.TextStim(glb.UI_WIN, text=TEXT_TEXT, font = glb.PARAMETERS.text['font'], height=TEXT_HEIGHT, 
                       colorSpace='rgb255', color=TEXT_COLOR, alignText='center', units='norm')
DEF_TEXT_HEIGHT = glb.PARAMETERS.text['size']

def draw_text(Text:str, Pos:tuple=(0,0), Height:int=DEF_TEXT_HEIGHT, Color:tuple=(255,255,255)):
    global TEXT_COLOR, TEXT_HEIGHT, TEXT_TEXT, TEXT_POS

    if Color != TEXT_COLOR:
        TEXT.setColor(Color)
        TEXT_COLOR = Color
    
    if Pos != TEXT_POS:
        TEXT.setPos(Pos)
        TEXT_POS = Pos

    if Height != TEXT_HEIGHT:
        TEXT.setHeight(Height/TEXT_CONV)
        TEXT_HEIGHT = Height/TEXT_CONV
    
    if Text != TEXT_TEXT:
        TEXT.setText(Text)
        TEXT_TEXT = Text

    TEXT.draw()


IMAGE = visual.ImageStim(glb.UI_WIN, units='norm')
IMAGE_NAME = ''
IMAGE_POS = (0,0)
IMAGE_SIZE = (1,1)
def draw_image(Image:str, Pos:tuple=(0,0), Size=None):
    global IMAGE_NAME, IMAGE_POS, IMAGE_SIZE

    if Image != IMAGE_NAME:
        IMAGE.setImage(Image)
        IMAGE_NAME = Image
    
    if Pos != IMAGE_POS:
        IMAGE.setPos(Pos)
        IMAGE_POS = Pos
    
    if Size != IMAGE_SIZE:
        IMAGE.setSize(Size)
        IMAGE_SIZE = Size

    IMAGE.draw()


# SLIDER = visual.Slider(glb.UI_WIN, style=['rating', 'triangleMarker'])
SLIDER = visual.Slider(
            win=glb.UI_WIN,
            size=(0.8, 0.1),
            pos=(0, -0.7),
            labels=[str(i) for i in range(1, 11)],  # Scale labels from 1 to 10
            ticks=list(range(1, 11)),  # Ticks from 1 to 10
            granularity=1,
            style=['rating', 'triangleMarker'],
            labelHeight=0.04  # Adjust label font size for spacing
    )
def draw_slider(Reset:bool=False):
    if Reset:
        SLIDER.reset()

    SLIDER.draw()


RECT = visual.Rect(glb.UI_WIN, colorSpace='rgb255')
RECT_FILLCOLOR = False
RECT_LINECOLOR = False
RECT_WIDTH = 0.5
RECT_HEIGHT = 0.5
RECT_POS = (0,0)
RECT_OPACITY = 1
def draw_rect(FillColor:tuple=(255,255,255), LineColor:tuple=False, Width:float=0.1, Height:float=0.1, Pos:tuple=(0,0), Opacity:float=1):
    global RECT_FILLCOLOR, RECT_LINECOLOR, RECT_WIDTH, RECT_HEIGHT, RECT_POS, RECT_OPACITY
    if FillColor != RECT_FILLCOLOR:
        RECT.setFillColor(FillColor)
        RECT_FILLCOLOR = FillColor

    if LineColor != RECT_LINECOLOR:
        RECT.setLineColor(LineColor)
        RECT_LINECOLOR = LineColor

    if Width != RECT_WIDTH:
        RECT.setWidth(Width)
        RECT_WIDTH = Width
    
    if Height != RECT_HEIGHT:
        RECT.setHeight(Height)
        RECT_HEIGHT = Height

    if Pos != RECT_POS:
        RECT.setPos(Pos)
        RECT_POS = Pos
    
    if Opacity != RECT_OPACITY:
        RECT.setOpacity(Opacity)
        RECT_OPACITY = Opacity

    RECT.draw()















# def load_partner_image(UI_WIN, image_folder):
#     """
#     Load a random partner image from the specified folder.
#     Parameters:
#     ----------
#     UI_WIN : psychopy.visual.Window
#         Window object where the image will be displayed.
#     image_folder : str
#         Path to the folder containing partner images.
#     Returns:
#     --------
#     psychopy.visual.ImageStim
#         The randomly selected partner image with consistent display settings.
#     """
#     # List all image files in the folder
#     image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
#     chosen_image = random.choice(image_files)
#     image_path = os.path.join(image_folder, chosen_image)

#     # Return the ImageStim object with specified display settings
#     return visual.ImageStim(
#         UI_WIN,
#         image=image_path,
#         units="norm",  # Normalized units for consistent size on different screens
#         pos=(0, 0.5),  # Position image towards the top of the screen
#         size=(0.8, 0.8)  # Make image smaller to fit comfortably on the screen
#     )

# def create_text_stimuli(UI_WIN, PARAMETERS, text_content, pos=(0, 0)):
#     """
#     Creates a TextStim object for displaying text.
#     """
#     try:
#         return visual.TextStim(
#             win=UI_WIN,
#             text=text_content,
#             font=PARAMETERS.text.get('font', 'Arial'),  # Default to Arial if unspecified
#             color=PARAMETERS.text.get('color', [1, 1, 1]),  # Ensure color is in RGB format
#             colorSpace='rgb',
#             height=0.1,  # Default text height, should scale to 'norm' units
#             units='norm',
#             pos=pos
#         )
#     except Exception as e:
#         print(f"Error creating TextStim for '{text_content}': {e}")
#         return None


# def create_button(UI_WIN, label, pos):
#     """
#     Creates a button with a rectangle background and text overlay.
#     """
#     button_rect = visual.Rect(
#         win=UI_WIN,
#         width=0.6,
#         height=0.2,
#         pos=pos,
#         fillColor='blue',
#         lineColor='blue'
#     )
#     button_text = visual.TextStim(
#         win=UI_WIN,
#         text=label,
#         pos=pos,
#         height=0.08,
#         color='white'
#     )
#     return button_rect, button_text


# def create_trust_slider(UI_WIN):
#     """
#     Creates a slider to rate trustworthiness on a scale of 1 to 10.
#     """
#     trust_slider=visual.Slider(
#         win=UI_WIN,
#         size=(0.8, 0.1),
#         pos=(0, -0.7),
#         labels=[str(i) for i in range(1, 11)],  # Scale labels from 1 to 10
#         ticks=list(range(1, 11)),  # Ticks from 1 to 10
#         granularity=1,
#         style=['rating', 'triangleMarker'],
#         labelHeight=0.04  # Adjust label font size for spacing
#     )

#     # Instruction text above the slider
#     instructions_text = visual.TextStim(
#         win=UI_WIN,
#         text="Please rate the trustworthiness of your partner on the scale below. Move slider with trackpad to desired ranking and press ENTER",
#         pos=(0, -0.3),  # Position above the slider
#         height=0.07
#     )

#     # Add text labels for "Not Trustworthy," "Neutral," and "Trustworthy"
#     not_trustworthy_label =visual.TextStim(
#         win=UI_WIN,
#         text="Not Trustworthy",
#         pos=(-0.4, -0.6),  # Position to the left of the slider
#         height=0.05
#     )
    
#     neutral_label = visual.TextStim(
#         win=UI_WIN,
#         text="Neutral",
#         pos=(0, -0.6),  # Position centered under the slider
#         height=0.05
#     )
    
#     trustworthy_label = visual.TextStim(
#         win=UI_WIN,
#         text="Trustworthy",
#         pos=(0.4, -0.6),  # Position to the right of the slider
#         height=0.05
#     )
#     # Return the slider, instructions, and labels as a tuple
#     return trust_slider, instructions_text, not_trustworthy_label, neutral_label, trustworthy_label
