# IoT-Web-Framework
A framework for linking a arduino to a webbrowser, via a RS-232 Uart (Serial) interface and a Raspberry Pi or PC running a web server and provided python application.

Developed in conjunction with Hackerspace Adelaide. http://hackerspace-adelaide.org.au/

## src/server
A python3 Websocket server that forwards data between the web browser and a serial port on the running machine.

Note the PyLibs dir is licensed lgpl2.1

### Usage

## src/web
A web page that connects to the server and sends / recieves data from it and the arduino

### Usage
Add the file to the web server on your machine or just open the file in your browser.

## src/arduino
Some sample arduino code that Turns on / off the LED on pin 13.
