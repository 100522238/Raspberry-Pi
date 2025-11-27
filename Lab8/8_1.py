import os
import SSD1331
import RPi.GPIO as GPIO
import datetime
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from encoder import Encoder


"""Constants config"""
PHOTOS_DIR = "/home/pi/photos/"
INTERVAL = 5  # seconds
DISPLAY_w = 96
DISPLAY_h = 64
SHOW_DATE = True
DRAW_FRAME = True

GPIO.setmode(GPIO.BCM)


"""OLED Display config"""

disp = SSD1331.SSD1331()
disp.Init()
disp.clear()  # Clear display

def load_photo_list(path):
    #Returns a list of valid images of the path
    valid_ext = (".jpg", ".jpeg", ".png")
    files = [f for f in os.listdir(path) if f.lower().endswith(valid_ext)]
    files.sort()
    return files

def draw_border(draw):
    # Draw a border around the display
    draw.rectangle((0, 0, DISPLAY_w - 1, DISPLAY_h - 1), outline="BLUE")

def add_date(draw, filepath):
    # Add the current date and time to the image
    ts = os.path.getmtime(filepath)
    date_text = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    font = ImageFont.load_default()
    draw.text((2, DISPLAY_h - 10), date_text, font=font, fill="WHITE")

def prepare_image(filepath):
    # Open an image file and prepare it for display
    img = Image.open(filepath)
    img = img.convert("RGB")
    img = img.resize((DISPLAY_w, DISPLAY_h))
    draw = ImageDraw.Draw(img)

    if DRAW_FRAME:
        draw_border(draw)

    if SHOW_DATE:
        add_date(draw, filepath)

    return img

"""Main loop"""

def main():
    enc = Encoder(26, 19)
    
    photos = load_photo_list(PHOTOS_DIR)
    if len(photos) == 0:
        print("No photos found in directory:", PHOTOS_DIR)
        return
    
    index = 0

    last_change = datetime.now()
    next_photo = False

    while True:
        now = datetime.now()
        elapsed = (now - last_change).total_seconds()

        #Claculate index based on encoder value
        final_index = (index + enc.value) % len(photos)
        filepath = os.path.join(PHOTOS_DIR, photos[final_index]) # Creates the path of the photo selected

        img = prepare_image(filepath)
        disp.ShowImage(img)

        #Time management for showing next photo
        if elapsed >= INTERVAL:
            last_change = now
            next_photo = True


        #next index
        if next_photo:
            index = (index + 1) % len(photos)
            next_photo = False


if __name__ == "__main__":
    main()