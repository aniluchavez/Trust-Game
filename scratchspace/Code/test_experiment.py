# test_image_text_rendering.py
from psychopy import core, visual
from stimuli import load_partner_image, create_text_stimuli, create_trust_slider
import globals as glb

def test_image_and_text():
    PARAMETERS = glb.PARAMETERS  # Access PARAMETERS from globals
    UI_WIN = PARAMETERS.create_window()

    # Load partner image
    partner_image = load_partner_image(UI_WIN, PARAMETERS.stimuli['imageFolder'])

    # Create text stimulus for partner name
    partner_name_text = create_text_stimuli(
        UI_WIN, PARAMETERS, text_content="John Pork", pos=(0, 0)
    )

    # Create trustworthiness slider
    trust_slider = create_trust_slider(UI_WIN)

    # Draw image, text, and slider together
    if partner_image:
        partner_image.draw()
    if partner_name_text:
        partner_name_text.draw()
    if trust_slider:
        trust_slider.draw()
    
    # Display everything on the screen
    UI_WIN.flip()
    core.wait(15)  # Display for 2 seconds
    
    # Close the window after the test
    UI_WIN.close()
    core.quit()

if __name__ == "__main__":
    test_image_and_text()
