# marquee.py
# wifi controlled message scroller
#
# Author: Joseph G. Wezensky
# License: MIT License (https://opensource.org/licenses/MIT)
#
# Wiring...
# Wemos D1 Mini  max7219 8x8 LED Matrix
#    5V          VCC
#    GND         GND
#    D7 MOSI     DIN
#    D8          CS
#    D5 SCK      CLK

import uasyncio as asyncio
import uos
import socket
import network
import dnsquery
from drivers import max7219m
from machine import Pin, SPI

webroot = 'wwwroot'
default = 'marquee.html'
redirect_file = '/wwwroot/captive.html'
ssid = 'MyMarquee'
message = "Connect your wifi to MyMarquee"
dic = {"%21":"!","%22":'"',"%23":"#","%24":"$","%26":"&","%27":"'","%28":"(","%29":")","%2A":"*","%2B":"+","%2C":",","%2F":"/","%3A":":","%3B":";","%3D":"=","%3F":"?","%40":"@","%5B":"[","%5D":"]","%7B":"{","%7D":"}"}

@asyncio.coroutine
def capture_dns(udps, ip):
    while True:
        try:
            data, addr = udps.recvfrom(1024)
            p=dnsquery.DNSQuery(data)
            udps.sendto(p.respuesta(ip), addr)
        except:
            pass
            #print('no dns')
        await asyncio.sleep_ms(300)

@asyncio.coroutine
def scroll_message(display):
    global message
    while True:
        try:
            start = 33
            extent = 0 - (len(message) * 8) - 32

            for i in range(start, extent, -1):
                display.fill(0)
                display.text(message, i, 0, 1)
                display.show()
                await asyncio.sleep_ms(25)

            await asyncio.sleep(1)
        except:
            pass

        await asyncio.sleep_ms(100)

def urldecode(str):
    global dic
    for k,v in dic.items(): str=str.replace(k,v)
    return str

# Breaks an HTTP request into its parts and boils it down to a physical file (if possible)
def decode_path(req):
    global message
    global default
    cmd, headers = req.decode("utf-8").split('\r\n', 1)
    parts = cmd.split(' ')
    method, path = parts[0], parts[1]
    # remove any query string
    query = ''
    r = path.find('?')
    if r > 0:
        query = path[r:]
        path = path[:r]
    # check for use of default document
    if path == '/':
        path = default
    else:
        path = path[1:]

    #print('METHOD:' + method)
    #print('PATH  :' + path)
    #print('QRYSTR:' + query)

    if path == default and query != '' and query.startswith('?msg='):
        message = urldecode(query[5:].replace('+', ' '))
        print('MSG:"' + message + '"')

    # return the physical path of the response file
    return webroot + '/' + path

# Looks up the content-type based on the file extension
def get_mime_type(file):
    if file.endswith(".html"):
        return "text/html", False
    if file.endswith(".css"):
        return "text/css", True
    if file.endswith(".js"):
        return "text/javascript", True
    if file.endswith(".png"):
        return "image/png", True
    if file.endswith(".gif"):
        return "image/gif", True
    if file.endswith(".jpeg") or file.endswith(".jpg"):
        return "image/jpeg", True
    if file.endswith(".pdf"):
        return "application/pdf", True
    return "text/plain", False

# Quick check if a file exists
def exists(file):
    try:
        s = uos.stat(file)
        return True
    except:
        return False    

@asyncio.coroutine
def serve_http(reader, writer):
    try:
        file = decode_path((yield from reader.read()))

        if exists(file):
            mime_type, cacheable = get_mime_type(file)
            yield from writer.awrite("HTTP/1.0 200 OK\r\n")
            yield from writer.awrite("Content-Type: {}\r\n".format(mime_type))
            if cacheable:
                yield from writer.awrite("Cache-Control: max-age=86400\r\n")
            yield from writer.awrite("\r\n")
        else:
            yield from writer.awrite("HTTP/1.0 200 OK\r\n")
            yield from writer.awrite("Content-Type: text/html\r\n")
            yield from writer.awrite("\r\n")
            file = redirect_file

        buf = bytearray(512)
        f = open(file, "rb")
        size = f.readinto(buf)
        while size > 0:
            yield from writer.awrite(buf, sz=size)
            size = f.readinto(buf)
        f.close()

    except:
        #import machine
        #machine.reset()
        pass
    finally:
        yield from writer.aclose()

def initialize():
    global ssid

    # shutdown any local wifi connect
    sta = network.WLAN(network.STA_IF)
    if sta.active():
        sta.active(False)
        while sta.isconnected():
            pass

    # startup the device as an AP
    ap = network.WLAN(network.AP_IF)
    if not ap.active():
        ap.active(True)
        ap.config(essid=ssid, password="", authmode=1)

    return ap.ifconfig()[0]

def shutdown():
    sta = network.WLAN(network.STA_IF)
    if sta.active():
        sta.active(False)
        while sta.isconnected():
            pass
    ap = network.WLAN(network.AP_IF)
    if ap.active():
        ap.active(False)

def run():
    # setup as Access point
    ip = initialize()

    # prepare to capture DNS requests
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.setblocking(False)
    udps.bind(('',53))

    # prepare to scroll text
    spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
    display = max7219m.Max7219M(spi, Pin(15), 4)
    display.brightness(7)

    # load up the coros and run
    loop = asyncio.get_event_loop()
    loop.create_task(capture_dns(udps, ip))
    loop.create_task(scroll_message(display))
    loop.create_task(asyncio.start_server(serve_http, "0.0.0.0", 80, 20))
    loop.run_forever()

    # if we ever finish
    loop.close()
    udps.close()

    #shutdown access point
    shutdown()

run()