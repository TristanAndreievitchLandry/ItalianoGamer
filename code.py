import time
import random
import board
import displayio
from adafruit_display_text import label
import terminalio
from analogio import AnalogIn
import audioio
import audiomp3
import neopixel
import keypad
import digitalio


# Dictionary of Italian words and their French translations
dictionary = {
    "Casa": "maison",
    "gatto": "chat",
    "sole": "soleil",
    "mela": "pomme",
    #   "precipitevolissimevolmente": "tres rapidement",
    "fino a oggi": "jusqu'a aujourd'hui",
    "vicenda": "aventure",
    "spiega": "expliquer",
    "escono": "ils sortent",
    "referti": "rapports",
    "ricovero": "legiste",
    "ripercorrere": "retracer",
    "cosiddetto": "soi-disant",
    "spesso": "souvent",
    "cartelli": "pancartes",
    "smette": "cesser",
    "sottoposte": "soumise",
    "tra cui": "parmi lesquels",
    "per procura": "par procuration",
    "fronteggiando": "oriente vers",
    "respingere": "rejeter",
    "legame": "lien",
    "sparizioni": "disparitions",
    "stupri": "viols",
    "accadde": "C'est arrive",
    "assediare": "assieger",
    "spiegato": "explique",
    "mai": "jamais",
    "fornisca": "apporter",
    "bensi": "mais",
    "rodato": "rode",
    "uccise": "tues",
    "assedio": "siege",
    "ferite": "blesses",
    "scagnatto": "lance",
    "lato": "cote",
    "affidano": "confie",
    "decine": "dizaines",
    "fonti": "sources",
    "sedare": "calmer",
    "passo falso": "faux pas",
    "tetti": "toits",
    "rubar": "voler",
    "accontar": "regler",
    "dai": "allez",
    "eccoci": "nous sommes ici",
    "durano": "durent",
    "quindi": "donc",
    "festeggia": "celebrer",
    "in anticipo": "a l'avance",
    "svegliato": "reveille",
    "scesi": "descendu",
    "ad ogni modo": "de toute facon",
    "ghiaccio": "glace",
    "ovviamente": "de toute evidence",
    "richiudere": "fermer",
    "condividere": "partager",
    "magari": "esperons",
    "ascoltano": "ecoutent",
    "suonovano": "ils ont joue",
    "famosissima": "tres celebre",
    "ballavano": "ils ont danse",
    "palco": "estrade",
    "credo": "je crois",
    "affitando": "location",
    "tra l'altro": "en outre",
    "chiacchierata": "lunga conversazione alla buona",
    "a contato": "en contact",
    "attimo": "moment",
    "piani": "plans",
    "butare giu": "espressione idiomatica colloquiale: scrivere",
    "ogni": "tous",
    "staccare dal lavoro": "deconnecter du travail",
    "sedere": "s'asseoir",
    "addiritura": "vraiment",
    #   "che cosa fai oggi": "que fais tu aujourd'hui",
    "si integrano a vicenda": "se completent",
    "mandare": "envoyer",
    "invece": "au lieu",
    "solito": "habituel",
    "ridisceso": "descendu",
    # Add more Italian words and their translations here
}


###################################################################

# flashing leds stuff

# Set up the neopixel strip
strip = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness=0.1)

# Define the colors for flashing
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# Function to flash the lights with a specific color


def flash_lights(color, duration):
    strip.fill(color)
    strip.show()
    time.sleep(duration)
#########################################################################

# audio stuff


# enable the speaker on the board
spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = True
tone_volume = 0.05  # that line does not work

# Load the win sound
win_sound = audiomp3.MP3Decoder(open("win.mp3", "rb"))
end_sound = audiomp3.MP3Decoder(open("end.mp3", "rb"))

# Function to play sound

def play_sound(sound):
    audio = audioio.AudioOut(board.A0)
    audio.play(sound)
    while audio.playing:
        pass
    audio.deinit()

#########################################################################

# controls stuff
# see Adafruit py file of the same name on git hub


# init keypad on PyGamer
k = keypad.ShiftRegisterKeys(
    clock=board.BUTTON_CLOCK,
    data=board.BUTTON_OUT,
    latch=board.BUTTON_LATCH,
    key_count=8,
    value_when_pressed=True,
)

# advanced electronic stuff
# I must read Howowitz & Read

# return a value from zero to 127


def getVoltage(pin):
    return int((pin.value / 65536) * 127)
    return int((pin.value / 65536) * 127)

# Function to be triggered when key 1 is pressed


def function_key_1():
    play_sound(end_sound)

##########################################################################

# screen stuff


# Create the display context
display = board.DISPLAY
splash = displayio.Group()

# Colors
Green2 = 0x008C45
White2 = 0xFFFFFF
Red2 = 0xB80D24
Black = 0x000000

# Make a black background color fill
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = Black
bg_sprite = displayio.TileGrid(
    color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

##########################################################################

# the dictionary stuff

# Create a text label for the Italian word
italian_label = label.Label(
    terminalio.FONT,
    text="",
    color=White2,
    anchor_point=(0.5, 0.5),
    anchored_position=(display.width // 2, display.height // 2),
)

# Create a text label for the French translation
trans_label = label.Label(
    terminalio.FONT,
    text="",
    color=Green2,
    anchor_point=(0.5, 0.5),
    anchored_position=(display.width // 2, display.height // 2),
)


def wrap_text(text, width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) <= width:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())

    return "\n".join(lines)


##########################################################################

# first we display the Italian flag, 'cause, you know?

def display_italian_flag():
    # Create the display object
    display = board.DISPLAY
    # Create the color palette for the Italian flag
    color_palette = displayio.Palette(3)
    color_palette[0] = Green2
    color_palette[1] = White2
    color_palette[2] = Red2

    # Create the bitmap with the Italian flag colors
    bitmap = displayio.Bitmap(
        display.width, display.height, len(color_palette))

    # Fill the bitmap with the Italian flag colors
    for x in range(display.width):
        for y in range(display.height):
            if x < display.width // 3:
                bitmap[x, y] = 0  # Green
            elif x < display.width * 2 // 3:
                bitmap[x, y] = 1  # White
            else:
                bitmap[x, y] = 2  # Red

    # Create a TileGrid with the bitmap and color palette
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=color_palette)

    # Create a Group and add the TileGrid
    group = displayio.Group()
    group.append(tile_grid)

    # Show the Group on the display
    display.show(group)
    play_sound(win_sound)
    # Wait for 3 seconds
    # time.sleep(2)

    # Clear the display
    blank_bitmap = displayio.Bitmap(display.width, display.height, 1)
    blank_palette = displayio.Palette(1)
    blank_palette[0] = Black
    blank_sprite = displayio.TileGrid(blank_bitmap, pixel_shader=blank_palette)
    group = displayio.Group()
    group.append(blank_sprite)
    display.show(group)


display_italian_flag()

#################################################################################

# then we display one Italian word, followed by the translation after joystick moved to right, left goes back to last Italian word.

splash.append(italian_label)  # Add Italian label to display initially

# Initialize the analog joystick
joy_x = AnalogIn(board.JOYSTICK_X)
joy_y = AnalogIn(board.JOYSTICK_Y)

# Show the display
display.show(splash)

italian_words = list(dictionary.keys())
current_word_index = random.randint(0, len(italian_words) - 1)
display_translation = False
last_move_time = time.monotonic()
translation_count = 0


while True:
    # Read joystick values
    x_value = joy_x.value
    y_value = joy_y.value
    event = k.events.get()  # check for button event
    if event:
        if event.pressed and event.key_number == 1:
            function_key_1()  # Call the function when key 1 is pressed

    # Check if enough time has passed since the last move
    if time.monotonic() - last_move_time < 0.2:
        continue

    # Check if joystick is moved to the right
    if x_value > 60000:
        # Move to next Italian word or show translation
        if not display_translation:
            display_translation = True
            wrap_trans = wrap_text(
                dictionary[italian_words[current_word_index]], 9)
            trans_label.text = wrap_trans.lower()
            # Center the wrapped text
            trans_label.anchor_point = (0.5, 0.5)
            trans_label.anchored_position = (
                display.width // 2, display.height // 2)
            splash.remove(italian_label)  # Remove Italian label from display
            splash.append(trans_label)  # Add translation label to display
            translation_count += 1
            if translation_count % 10 == 0:
                play_sound(end_sound)
                # Flash red, green, and white for 3 seconds
                flash_lights(green, 0.33)    # Flash green for x second
                flash_lights(white, 0.33)    # Flash white for x second
                flash_lights(red, 0.33)      # Flash red for x second
                # Turn off the lights
                strip.fill((0, 0, 0))
                strip.show()

        else:
            display_translation = False
            current_word_index = (current_word_index + 1) % len(italian_words)
            italian_label.text = italian_words[current_word_index]
            splash.remove(trans_label)  # Remove translation label from display
            splash.append(italian_label)  # Add Italian label back to display

        # Adjust font size based on word length
        italian_word_length = len(italian_label.text)
        french_word_length = len(trans_label.text)

        if italian_word_length <= 9:
            italian_font_size = 3
        elif italian_word_length > 9:
            italian_font_size = 2
        else:
            italian_font_size = 3

        if french_word_length <= 9:
            french_font_size = 3
        elif french_word_length > 9:
            french_font_size = 2
        else:
            french_font_size = 3

        italian_label.scale = italian_font_size
        trans_label.scale = french_font_size

        # Update the last move time
        last_move_time = time.monotonic()

    # Check if joystick is moved to the left
    if x_value < 2000:
        # Move to previous Italian word
        if display_translation:
            display_translation = False
            wrapped_italian_word = wrap_text(
                italian_words[current_word_index], 9)
            italian_label.text = wrapped_italian_word.lower()
            # Center the wrapped text
            italian_label.anchor_point = (0.5, 0.5)
            italian_label.anchored_position = (
                display.width // 2, display.height // 2)
            splash.remove(trans_label)  # Remove translation label from display
            splash.append(italian_label)  # Add Italian label back to display

        # Adjust font size based on word length
        italian_word_length = len(italian_label.text)
        french_word_length = len(trans_label.text)

        if italian_word_length <= 8:
            italian_font_size = 3
        elif italian_word_length > 8:
            italian_font_size = 2
        else:
            italian_font_size = 3

        if french_word_length <= 8:
            french_font_size = 3
        elif french_word_length > 8:
            french_font_size = 2
        else:
            french_font_size = 3

        italian_label.scale = italian_font_size
        trans_label.scale = french_font_size

        # Update the last move time
        last_move_time = time.monotonic()
