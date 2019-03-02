# WifiMarquee
An ESP8266 based scrolling marquee written in MicroPython that can be controlled through a web-based wifi interface.

<p align="center">
  <img src="https://github.com/joewez/WifiMarquee/blob/master/display.gif" alt="Screenshot"/>
</p>

# Requirements:

  MicroPython 1.10 or later

# Wiring:

**Wemos D1 Mini**  <-->  **MAX7219 LED Matrix**
 
    5V         <-->     VCC
    
    GND        <-->     GND
    
    D7 (MOSI)  <-->     DIN
    
    D8         <-->     CS
    
    D5 (SCK)   <-->     CLK

# Credit:

MicroPython MAX7219 Driver:

https://github.com/mcauser/micropython-max7219

DNS Server Code and Stucture:

https://github.com/amora-labs/micropython-captive-portal

