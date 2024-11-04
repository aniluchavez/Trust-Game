from psychopy import visual
import globals as glb

# PHOTODIODE CODE
PHOTODIODE = visual.Rect(glb.UI_WIN, fillColor='white', lineColor='white', width=0.083, height=0.166, pos=(-0.958, -0.9166))


# CODE FOR THE TEXT STIMULUS
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


# CODE FOR THE IMAGE STIMULUS
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


# CODE FOR THE SLIDER STIMULUS
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


# CODE FOR THE RECANGULAR STIMULUS
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