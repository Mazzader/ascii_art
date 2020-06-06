import curses
from PIL import Image as PilImage, ImageDraw as PilImageDraw
import math

def getChar(inputInt):
    chars = r"@B&#WMZO0QbdpqwmoazunxrctiI1?l!+~;:-_,`."[::-1]
    charArray = list(chars)
    charLength = len(charArray)
    interval = charLength / 256
    return charArray[math.floor(inputInt * interval)]

def main_convertation_w(img):
    text_file = open('result.txt', 'w')
    scaleFactor = 0.1
    oneCharWidth = 8
    oneCharHeight = 12
    width, height = img.size[0], img.size[1]
    img.resize((int(scaleFactor * width), int(scaleFactor * height * (oneCharWidth / oneCharHeight))),
               PilImage.NEAREST)
    pixels = img.load()
    outputImage = PilImage.new('RGB', (oneCharWidth * width, oneCharHeight * height), color=(30, 30, 30))
    d = PilImageDraw.Draw(outputImage)

    for i in range(height):
        for j in range(width):
            r, g, b = pixels[j, i]
            h = int(r / 3 + g / 3 + b / 3)
            pixels[j, i] = (h, h, h)
            text_file.write(getChar(h))
            d.text((j * oneCharWidth, i * oneCharHeight), getChar(h),
                   fill=(255,255,255))
        text_file.write('\n')
    outputImage.save('output.png')

def main_convertation_bw(img):
    text_file = open('result.txt', 'w')
    scaleFactor = 0.1
    oneCharWidth = 8
    oneCharHeight = 12
    width, height = img.size[0], img.size[1]
    img.resize((int(scaleFactor * width), int(scaleFactor * height * (oneCharWidth / oneCharHeight))),
               PilImage.NEAREST)
    pixels = img.load()
    outputImage = PilImage.new('RGB', (oneCharWidth * width, oneCharHeight * height), color=(30, 30, 30))
    d = PilImageDraw.Draw(outputImage)

    for i in range(height):
        for j in range(width):
            r, g, b = pixels[j, i]
            h = int(r / 3 + g / 3 + b / 3)
            pixels[j, i] = (h, h, h)
            text_file.write(getChar(h))
            d.text((j * oneCharWidth, i * oneCharHeight), getChar(h), fill=(int(r * 0.2126) + int(g * 0.7152) + int(b * 0.0722),
                                                                            int(r * 0.2126) + int(g * 0.7152) + int(b * 0.0722),
                                                                            int(r * 0.2126) + int(g * 0.7152) + int(b * 0.0722)))
        text_file.write('\n')
    outputImage.save('output.png')

def main_convertation(img):
    width, height = img.size[0], img.size[1]
    text_file = open('result.txt', 'w')
    scaleFactor = 0.1
    oneCharWidth = 8
    oneCharHeight = 12
    img.resize((int(scaleFactor * width), int(scaleFactor * height * int(oneCharWidth / oneCharHeight))),
               PilImage.NEAREST)
    pixels = img.load()
    outputImage = PilImage.new('RGB', (oneCharWidth * width, oneCharHeight * height), color=(30, 30, 30))
    d = PilImageDraw.Draw(outputImage)

    for i in range(height):
        for j in range(width):
            r, g, b = pixels[j, i]
            h = int(r / 3 + g / 3 + b / 3)
            pixels[j, i] = (h, h, h)
            text_file.write(getChar(h))
            d.text((j * oneCharWidth, i * oneCharHeight), getChar(h), fill=(r,g,b))
        text_file.write('\n')
    outputImage.convert('LA')
    outputImage.save('output.png')

def main(scr, *args):
    # -- Perform an action with Screen --
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    scr.border(0)
    curses.echo()
    scr.addstr(5, 5, 'Hello from Curses!',  curses.color_pair(1))
    scr.addstr(6, 5, 'Press ctrl+x to close this screen',  curses.color_pair(1))
    scr.addstr(8,5, 'type path to you image need to convert here: ',  curses.color_pair(1))
    path = scr.getstr(8, 50, 30)
    img = PilImage.open(path)
    mode_str = 'type mode to convert. Press g if you want grayscale or c if you need colored or w if you need white'
    scr.addstr(10, 5, 'type mode to convert. Press g if you want grayscale or c if you need colored or w if you need white', curses.color_pair(1))
    mode = scr.getstr(10, 5 + len(mode_str), 2)

    if mode == b'g':
        main_convertation_bw(img)
        scr.addstr(15,10,'success', curses.color_pair(1))
    elif mode == b'c':
        main_convertation(img)
        scr.addstr(15, 10, 'success', curses.color_pair(1))
    elif mode == b'w':
        main_convertation_w(img)
        scr.addstr(15, 10, 'success', curses.color_pair(1))
    else:
        scr.addstr(10, 10, 'exeption, pls rerun program and try again', curses.color_pair(1))
    while True:
        # stay in this loop till the user presses 'ctrl+x'
        ch = scr.getch()

        if ch == 24:
            break


curses.wrapper(main)