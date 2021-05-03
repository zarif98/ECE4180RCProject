<p align="center"><img width=12.5% src="build/images/rc.jpg"></p>
<p align="center"><img width=60% src="build/images/title.png"></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
[![Build Status](https://travis-ci.org/anfederico/Clairvoyant.svg?branch=master)](https://travis-ci.org/anfederico/Clairvoyant)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/anfederico/Clairvoyant.svg)](https://github.com/zarif98/ECE4180RCProject/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# To Do (Delete after)

- ~~Team members~~
- ~~parts list~~
- schematic
- source code
- photos & videoes
- Powerpoint for video presentation (6 slides max) final slide for further ideas

Checkout the website: http://zarifandr.com/ECE4180RCProject/

## Basic Overview

Build an RC car using the shadow chassis with Xbox controls and Pi cam at the front. The Pi streams video onto a web app
accessible by anyone on the same wifi network.

<br>

## Latest Development Changes

```bash
git clone https://github.com/zarif98/ECE4180RCProject.git
```

# Setup

## Assembling the Shadow Chasis Robot

[![SparkFun - Shadow Chassis Assembly Guide](https://i.imgur.com/7mptFid.jpeg)](http://www.youtube.com/watch?v=aJRYTqZu5OE&t "SparkFun - Shadow Chassis Assembly Guide")

## Connecting the Controller

Follow these steps to connect the Xbox One controller to the Raspberry Pi:

```
https://pimylifeup.com/xbox-controllers-raspberry-pi/
```

The source code to run the controller can be found in the Pi-Controller folder. The Pi-contoller code looks for 6 different inputs: X and Y of the left analog joystick (for driving), Left and Right Triggers (for moving the camera), and A and B button (for playing sounds). This code runs simultaneously with the Pi camera stream code.

## Streaming and Pi Camera

The RC car is equipped with a Pi cam at the front of the car. The camera is powered by a Raspberry Pi 4. The streaming website is written in Flask and interfaces with the camera. I would recommend running the website on a phone hotspot rather than GT wifi. Your website address should look something similar to this:

```
<raspberry_pi_ip:5000>
```

The Pi cam was also equipped with motion detection due to the fact that object detection runs at a measly 2fps on the Pi 4. We can maintain our 24fps on the Raspi 4 with motion detection running at 5fps. Fork over the Pi Stream folder to run the code and hit main.py

# Hardware

## Parts List

<br>
<br>

|            Part Name             | Quantity |
| :------------------------------: | :------: |
|           mbed LPC1768           |    1     |
|  Hobby DC Gear Motor - 140 rpm   |    2     |
|       Shadow Robot Chassis       |    1     |
|      Sparkfun Dual H Bridge      |    1     |
|          Battery Holder          |    1     |
|       Xbox One Controller        |    1     |
|          Raspberry Pi 4          |    1     |
|      Raspberry Pi Cam V2.1       |    1     |
|      HC-SR04 (Sonar Sensor)      |    2     |
|        Speaker PCB Mount         |    1     |
| SparkFun Mono Audio Amp Breakout |    1     |
|      Anker Portable Battery      |    1     |
|         Micro Servo SG90         |    1     |

<br>
<br>

## Wheel Motors and H-Bridge Pinouts

| Mbed | Dual H-Bridge | Left DC Motors | Right DC Motors | Battery |
| :--: | :-----------: | :------------: | :-------------: | :-----: |
| Vout |   Vcc, STBY   |       nc       |       nc        |   nc    |
|  nc  |      Vm       |       nc       |       nc        |   6V+   |
| GND  |      GND      |       nc       |       nc        |   GND   |
| P26  |     PWMB      |       nc       |       nc        |   nc    |
| P25  |     PWMA      |       nc       |       nc        |   nc    |
| P20  |      AI1      |       nc       |       nc        |   nc    |
| P23  |      AI2      |       nc       |       nc        |   nc    |
| P22  |      BI2      |       nc       |       nc        |   nc    |
| P21  |      BI1      |       nc       |       nc        |   nc    |
|  nc  |      A01      |       +        |       nc        |   nc    |
|  nc  |      A02      |       -        |       nc        |   nc    |
|  nc  |      B01      |       nc       |        +        |   nc    |
|  nc  |      B02      |       nc       |        -        |   nc    |

## Speaker and Mono Audio Amp Pinouts

| Mbed | Mono Audio Amp | Speaker | Battery |
| :--: | :------------: | :-----: | :-----: |
| P18  |      IN+       |   nc    |   nc    |
| GND  |   PWR-, IN-    |   nc    |   GND   |
|  nc  |      OUT+      |    +    |   nc    |
|  nc  |      OUT-      |    -    |   nc    |

## Left Side Sonar Sensor Pinouts

| Mbed | Left HC-SR04 | Battery |
| :--: | :----------: | :-----: |
| GND  |     GND      |   GND   |
|  nc  |     Vcc      |   6V+   |
|  P6  |     Trig     |   nc    |
|  P7  |     Echo     |   nc    |

## Right Side Sonar Sensor Pinouts

| Mbed | Right HC-SR04 | Battery |
| :--: | :-----------: | :-----: |
| GND  |      GND      |   GND   |
|  nc  |      Vcc      |   6V+   |
| P12  |     Trig      |   nc    |
| P13  |     Echo      |   nc    |

## Pi Camera Servo Motor

| Mbed | Micro Servo SG90 | Battery |
| :--: | :--------------: | :-----: |
| GND  |      Brown       |   GND   |
|  nc  |       Red        |   6V+   |
| P24  |      Orange      |   nc    |

## Contributing

Feel free to fork over and utilize our code for future projects. Our goal was to utilize the material that we accumulated over the semester and combine them into one project.

#### Team Members

- Nicole Komocsar
- Zarif Rahman
- Marcus Chan
- Alan Jin
