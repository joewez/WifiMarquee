# WifiMarquee
An ESP8266 based scrolling marquee written in MicroPython that can be controlled through a web-based wifi interface.

<p align="center">
  <img src="https://github.com/joewez/WifiMarquee/blob/master/display.gif" alt="Screenshot"/>
</p>

When powered on, the device acts as an open WiFi access point that you can connect to with any modern device with a browser. The device will behave like a captive portal and direct you to a web page where you may enter your custom message. Just click the Submit button and your message should immediately begin scrolling on the device.

# Requirements:

  MicroPython 1.10 or later

# Wiring:

<p align="center">
  <img src="https://github.com/joewez/WifiMarquee/blob/master/Pocket%20WiFi%20Marquee%20-%20Wiring%20Diagram.jpg" alt="Wiring"/>
</p>

**Wemos D1 Mini**  <-->  **MAX7219 LED Matrix**

```
    5V         <-->     VCC   
    GND        <-->     GND
    D7 (MOSI)  <-->     DIN
    D8         <-->     CS
    D5 (SCK)   <-->     CLK
```

# Installation:

On a device with MicroPython installed, put the following files on the device using some method such as AMPY...

```
  + /(root)
    + /drivers
      + max7219m.py
    + /wwwroot
      + captive.html
      + marquee.html
    dnsquery.py
    main.py
    marquee.py
```

For example, in Windows using AMPY, and the device is connected through COM3, you could use these commands...

```
ampy -p COM3 -b 115200 put dnsquery.py /dnsquery.py
ampy -p COM3 -b 115200 put main.py /main.py
ampy -p COM3 -b 115200 put marquee.py /marquee.py
ampy -p COM3 -b 115200 mkdir drivers
ampy -p COM3 -b 115200 put drivers\max7219m.py /drivers/max7219m.py
ampy -p COM3 -b 115200 mkdir wwwroot
ampy -p COM3 -b 115200 put wwwroot\captive.html /wwwroot/captive.html
ampy -p COM3 -b 115200 put wwwroot\marquee.html /wwwroot/marquee.html
```

Note: If installing on a fresh install of MicroPython, you may have to issue these commands at a REPL prompt before the new SSID takes affect...

```
import network
ap = network.WLAN(network.AP_IF)
ap.active(False)
```

# Enclosure  
  
https://www.thingiverse.com/thing:3464108  
  
# Credit:

MicroPython MAX7219 Driver:

https://github.com/mcauser/micropython-max7219

DNS Server Code and Structure:

https://github.com/amora-labs/micropython-captive-portal

