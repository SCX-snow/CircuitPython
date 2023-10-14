import ipaddress
import os
import ssl
import time
import adafruit_ntp
import adafruit_requests
import rtc
import socketpool
import wifi
import board
import displayio
import adafruit_imageload
import neopixel
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_led_animation.animation.colorcycle import ColorCycle


def get_wday(week_today):
    if week_today == 0:
        return "周一"
    elif week_today == 1:
        return "周二"
    elif week_today == 2:
        return "周三"
    elif week_today == 3:
        return "周四"
    elif week_today == 4:
        return "周五"
    elif week_today == 5:
        return "周六"
    elif week_today == 6:
        return "周日"


def get_weather():
    requests = adafruit_requests.Session(socketpool.SocketPool(wifi.radio), ssl.create_default_context())
    appid = os.getenv("appid")
    appsecret = os.getenv("appsecret")
    res = requests.get(
        'https://v0.yiketianqi.com/free/day?appid=%s&appsecret=%s&unescape=1' % (appid, appsecret)).json()
    return res['wea'], res['tem_night'], res['tem_day']


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

timer = label.Label(num_font, text='10:17', color=0x779649)
timer.x = 15
timer.y = 65
group.append(timer)

weather = label.Label(word_font, text='阴', color=0x3271ae)
weather.x = 10
weather.y = 110
group.append(weather)

temperature = label.Label(word_font, text='10℃-15℃', color=0x3271ae)
temperature.x = 60
temperature.y = 110
group.append(temperature)

ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")

while True:
    print('try to connect ' + password + '@' + ssid)
    wifi.radio.connect(ssid, password)
    if wifi.radio.ping(ipaddress.IPv4Address('114.114.114.114')) is not None:
        print('wifi connected')
        break
    print('wifi connect failed')
    time.sleep(1)

color_cycle = ColorCycle(neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3), 0.5)

rtc.RTC().datetime = adafruit_ntp.NTP(socketpool.SocketPool(wifi.radio), tz_offset=8, server='ntp.aliyun.com').datetime

time_now = time.localtime()

date.text = '%d月%d日' % (time_now.tm_mon, time_now.tm_mday)
week.text = get_wday(time_now.tm_wday)
wea, tem_night, tem_day = get_weather()
weather.text = wea
temperature.text = '%s℃-%s℃' % (tem_night, tem_day)
board.DISPLAY.show(group)
while True:
    time_now = time.localtime()
    timer.text = '%02d:%02d' % (time_now.tm_hour, time_now.tm_min)
    if time_now.tm_min == 0:
        wea, tem_night, tem_day = get_weather()
        weather.text = wea
        temperature.text = '%d℃-%d℃' % (tem_night, tem_day)
        if time_now.tm_hour == 0:
            date.text = '%d月%d日' % (time_now.tm_mon, time_now.tm_mday)
            week.text = get_wday(time_now.tm_wday)
    board.DISPLAY.show(group)
    color_cycle.animate()
