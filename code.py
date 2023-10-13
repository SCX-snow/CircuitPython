import board
import displayio
import adafruit_imageload
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

image, palette = adafruit_imageload.load('/resource/back.bmp', bitmap=displayio.Bitmap, palette=displayio.Palette)
tile_grid = displayio.TileGrid(image, pixel_shader=palette)

group = displayio.Group()
group.append(tile_grid)
board.DISPLAY.show(group)

word_font = bitmap_font.load_font('/resource/word.pcf')
num_font = bitmap_font.load_font('/resource/num.pcf')

date = label.Label(word_font, text='10月13日', color=0xee7959)
date.x = 10
date.y = 20
group.append(date)

week = label.Label(word_font, text='周五', color=0x45465e)
week.x = 120
week.y = 20
group.append(week)

time = label.Label(num_font, text='10:17', color=0x779649)
time.x = 15
time.y = 65
group.append(time)

weather = label.Label(word_font, text='阴', color=0x3271ae)
weather.x = 10
weather.y = 110
group.append(weather)

temperature = label.Label(word_font, text='10℃-15℃', color=0x3271ae)
temperature.x = 70
temperature.y = 110
group.append(temperature)

while True:
    pass
