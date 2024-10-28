from psychopy import visual, core
import os
import random

# Path to the image folder
image_folder = "/Users/aniluchavez/Documents/GitHub/Scratch/scratchspace/Images/CFD-MR"

# Function to create the PsychoPy window
def create_window():
    return visual.Window(
        size=(1024, 768), 
        fullscr=False, 
        units='norm',  # Normalized units for consistent positioning
        color=[0.5, 0.5, 0.5],  # Gray background
        colorSpace='rgb'
    )

# Function to load a random image from the folder and create an ImageStim
def load_partner_image(UI_WIN, folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    if not image_files:
        raise FileNotFoundError(f"No .jpg images found in directory {folder_path}")

    chosen_image = os.path.join(folder_path, random.choice(image_files))
    print(f"Chosen image for partner: {chosen_image}")  # Debugging print statement

    partner_image = visual.ImageStim(
        UI_WIN,
        image=chosen_image,
        pos=(0, 0.5),  # Position at the top-center
        size=(0.5, 0.5)  # Adjust size as needed
    )
    return partner_image

# Function to create a button with a rectangle background and text overlay
def create_button(UI_WIN, label, pos):
    # Create a rectangle background
    button_rect = visual.Rect(
        win=UI_WIN,
        width=0.3, 
        height=0.15,
        pos=pos,
        fillColor='blue',
        lineColor='white'
    )
    # Create text overlay
    button_text = visual.TextStim(
        win=UI_WIN,
        text=label,
        pos=pos,
        height=0.08,
        color='white'
    )
    return button_rect, button_text

# Main function to run the intro test with buttons
def run_intro_test():
    # Create window
    UI_WIN = create_window()

    # Load partner image
    partner_image = load_partner_image(UI_WIN, image_folder)

    # Create buttons
    keep_button = create_button(UI_WIN, label="Keep $1", pos=(-0.4, -0.5))
    give_button = create_button(UI_WIN, label="Give $3", pos=(0.4, -0.5))

    # Draw and display the partner image and buttons
    print("Displaying introductory screen with partner image and choice buttons.")
    partner_image.draw()
    
    # Draw each button (background rectangle first, then text overlay)
    keep_button[0].draw()  # Background for "Keep" button
    keep_button[1].draw()  # Text for "Keep" button
    give_button[0].draw()  # Background for "Give" button
    give_button[1].draw()  # Text for "Give" button

    # Flip the window to show everything on screen
    UI_WIN.flip()
    core.wait(2)  # Display for 2 seconds

    # Close the window after display
    UI_WIN.close()
    core.quit()

# Run the test
if __name__ == "__main__":
    run_intro_test()
