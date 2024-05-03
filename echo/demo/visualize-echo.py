from pynput import keyboard
from playsound import playsound

# Boolean variable to track the state of the spacebar key
space_pressed = False

# Function to handle key press event
def on_press(key):
    global space_pressed
    
    try:
        print('pynput detect {0} pressed'.format(key.char))
        
        # Check if the pressed key is the spacebar
        if key == keyboard.Key.space and not space_pressed:
            space_pressed = True
            print("SPACE PRESS")
            # Call your function when spacebar is pressed
            function_on_spacebar_press()
            # Play sound when spacebar is pressed
            
    
    except AttributeError:
        print('pynput detect {0} pressed'.format(key))

# Function to handle key release event
def on_release(key):
    global space_pressed
    
    print('{0} released'.format(key))
    # Check if the released key is the spacebar
    if key == keyboard.Key.space:
        space_pressed = False
        print("SPACE RELEASE")
        # Call your function when spacebar is released
        function_on_spacebar_release()

    # Stop listener if escape key is pressed
    if key == keyboard.Key.esc:
        return False

# Define your functions to be called on spacebar press and release
def function_on_spacebar_press():
    playsound("../fresh-sounds/echo-listening.wav")
    print("Function on spacebar press")

def function_on_spacebar_release():
    playsound("../fresh-sounds/echo-heard.wav")
    print("Function on spacebar release")

# Start listener
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
