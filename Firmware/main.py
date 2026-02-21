import board
import os
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.rgb import RGB
from kmk.modules.oled import OLED
from PIL import Image

keyboard = KMKKeyboard()

rgb = RGB(
    num_pixels=16,
    data_pin=board.GP0,
)
keyboard.modules.append(rgb)

oled = OLED(
    width=128,
    height=32,
    i2c_scl=board.GP7,
    i2c_sda=board.GP6,
    timeout=30000,
)
keyboard.modules.append(oled)

ROWS = [
    board.GP1,  # Row 0 - pin 8
    board.GP2,  # Row 1 - pin 9
    board.GP4,  # Row 2 - pin 10
    board.GP3,  # Row 3 - pin 11
]

COLS = [
    board.GP26, # Col 0 - pin 1
    board.GP27, # Col 1 - pin 2
    board.GP28, # Col 2 - pin 3
    board.GP29, # Col 3 - pin 4
]

keyboard.matrix = KeysScanner(
    row_pins=ROWS,
    col_pins=COLS,
    value_when_pressed=False,
)

keyboard.keymap = [
    [
        KC.N1, KC.N2, KC.N3, KC.N4,
        KC.N5, KC.N6, KC.N7, KC.N8,
        KC.N9, KC.N0, KC.F1, KC.F2,
        KC.F3, KC.F4, KC.F5, KC.F6,
    ]
]

# OLED Animation 
animation_folder = "/animations"
bmp_frames = []

if os.path.exists(animation_folder):
    bmp_files = sorted(
        [f for f in os.listdir(animation_folder) if f.lower().endswith(".bmp")]
    )
    for f in bmp_files:
        path = os.path.join(animation_folder, f)
        bmp_frames.append(Image.open(path).convert("1"))

frame_index = 0

def oled_update(oled_device):
    global frame_index

    if bmp_frames:
        frame = bmp_frames[frame_index]
        oled_device.bitmap(frame)
        frame_index = (frame_index + 1) % len(bmp_frames)
    else:
        oled_device.text("Hackpad 4x4", 0, 0)

oled.tap = oled_update

if __name__ == "__main__":
    keyboard.go()