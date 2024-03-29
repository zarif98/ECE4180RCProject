<p align="center"><img width=12.5% src="build/images/rc.jpg"></p>
<p align="center"><img width=60% src="build/images/title.png"></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<!--![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
[![Build Status](https://travis-ci.org/anfederico/Clairvoyant.svg?branch=master)](https://travis-ci.org/anfederico/Clairvoyant)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/anfederico/Clairvoyant.svg)](https://github.com/zarif98/ECE4180RCProject/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)-->

Checkout the website: http://zarifandr.com/ECE4180RCProject/

## Basic Overview
<p align="center"><img width=60% src="build/images/robot.jpg"></p>
We built an RC car using the shadow chassis that was controlled with Xbox controls that were processed by the Raspberry Pi 4. There was also a Pi camera mounted on the front of the car on a servo motor that will turn. The Pi video stream is accessible on a web app accessible by anyone on the same wifi network. Two sonar systems were mounted on the left and right sides. If the sonars sensed anything on the sides of the car, it would cause the speakers to "honk". An Anker portable battery was used to power the Pi which in turn powered the entire system.

<br>

## Latest Development Changes

```bash
git clone https://github.com/zarif98/ECE4180RCProject.git
```

# Setup

## Assembling the Shadow Chasis Robot

Click on the image below to watch the video guide
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

<br>
Here's our Camera.py code. For more information click on the Pi-camera -stream-flask folder

```
import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as

class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
```

# Mbed Code

## Mbed 1: Servo and DC Motors
This is the code for the first mbed we used. This mbed was used to process the Pi serial commands from the Xbox controller that controlled the H-bridge for the two motors as well as the servo motor.

```
#include "mbed.h" // using namespace mbed; from Lab3-4_BT
#include "Motor.h" // #include "motordriver.h" // equivalent to DCMotor.h from class... might be more useful
//#include "uLCD_4DGL.h" // debugging
#include <cstdlib>
#include <string>
#include <string.h>
#include <ctype.h>
#include "Speaker.h"
#include "Servo.h"


Motor motor_right(p25, p20, p23); // pwm a, fwd (AI1), rev (AI2)
Motor motor_left(p26, p21, p22); // pwm b, fwd (BI1), rev (BI2)
Serial pi(USBTX, USBRX); // RawSerial
Servo cam_servo(p24); //Servo
DigitalOut mbed_led1(LED1);
DigitalOut mbed_led2(LED2);

const int MAX_BUFFER_SIZE = 128; // max number of possible chars -> pow2
char buffer[MAX_BUFFER_SIZE];
float buffer_to_int[6];
int spaces[6];

bool left = true;

int main() {
    mbed_led1 = 1;
    pi.baud(9600);
    while(1) {
        mbed_led1 = !mbed_led1;
        wait(0.2);
        int index = 0;
        buffer[0] = '\0';
        while (pi.readable() && index < MAX_BUFFER_SIZE) {
            buffer[index++] = pi.getc();
        }
        spaces[0] = -1;
        int i = 0;
        int count = 1;
        while (buffer[i]) {
            if (isspace(buffer[i])) {
                spaces[count++] = i;
            }
            i++;
        }
        for (int i = 0; i < 5; i++) {
            int starting = spaces[i] + 1;
            int ending = spaces[i+1];
            string s = "";
            while (starting < ending) {
                mbed_led2 = !mbed_led2;
                s += buffer[starting++];
            }
            buffer_to_int[i] = atof(s.c_str());
        }

        motor_left.speed(buffer_to_int[0]);
        motor_right.speed(-buffer_to_int[1]);

        float turn_left_cam = buffer_to_int[2];
        float turn_right_cam = buffer_to_int[3];
        if (turn_left_cam < 0 || turn_right_cam < 0 || // not triggering
                turn_left_cam > 0 && turn_right_cam > 0 || // holding both triggers
                cam_servo == 0.0 && turn_left_cam > 0 || // max left
                cam_servo == 1.0 && turn_right_cam > 0) { // max right
            float increm = (turn_left_cam > 0 ? -1 * cam_servo * 0.1 : -(1-cam_servo) * 0.1);
            float new_pos = cam_servo + increm;
            cam_servo = (new_pos > 1.0 ? 1.0 : (new_pos < 0.0 ? 0.0 : new_pos));
        }
    }
}
```
## Mbed 2: Sonar and Sound
This is the code for the second mbed we used. This mbed controlled the two sonars to trigger a "honk" if an object gets within a half of an inch of the RC car.
```
#include "mbed.h" // using namespace mbed; from Lab3-4_BT
#include "Motor.h" // #include "motordriver.h" // equivalent to DCMotor.h from class... might be more useful
#include "ultrasonic.h"
#include <stdlib.h>
#include <string.h>
#include "Speaker.h"

Speaker speaker(p18);

void dist(int distance) // left
{
    //put code here to execute when the distance has changed
    float x = float(distance)*(0.00328084);
    if (x  < .5) {
        speaker.PlayNote(500, 0.5, 0.5);
    }
}

void dist1(int distance) // right
{
    //put code here to execute when the distance has changed
    float x = float(distance)*(0.00328084);
    if (x  < .5) {
        speaker.PlayNote(500, 0.5, 0.5);
    }    
}

ultrasonic mu_left(p6, p7, .1, 1, &dist);
ultrasonic mu_right(p12, p13, .1, 1, &dist1);

int main() {
    
    mu_left.startUpdates();
    mu_right.startUpdates();
    
    while(1) {
        mu_right.checkDistance();
        mu_left.checkDistance();
    }   
}
```
# Hardware

## Parts List

<br>

|            Part Name             | Quantity |
| :------------------------------: | :------: |
|           mbed LPC1768           |    2     |
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

| Mbed 1 | Dual H-Bridge | Left DC Motors | Right DC Motors | Pin 2 on Pi | Pin 6 on Pi |
| :----: | :-----------: | :------------: | :-------------: | :---------: | :---------: |
|  Vout  |   Vcc, STBY   |       nc       |       nc        |     nc      |     nc      |
|   nc   |      Vm       |       nc       |       nc        |     5V+     |     nc      |
|  GND   |      GND      |       nc       |       nc        |     nc      |     GND     |
|  P26   |     PWMB      |       nc       |       nc        |     nc      |     nc      |
|  P25   |     PWMA      |       nc       |       nc        |     nc      |     nc      |
|  P20   |      AI1      |       nc       |       nc        |     nc      |     nc      |
|  P23   |      AI2      |       nc       |       nc        |     nc      |     nc      |
|  P22   |      BI2      |       nc       |       nc        |     nc      |     nc      |
|  P21   |      BI1      |       nc       |       nc        |     nc      |     nc      |
|   nc   |      A01      |       +        |       nc        |     nc      |     nc      |
|   nc   |      A02      |       -        |       nc        |     nc      |     nc      |
|   nc   |      B01      |       nc       |        +        |     nc      |     nc      |
|   nc   |      B02      |       nc       |        -        |     nc      |     nc      |

## Speaker and Mono Audio Amp Pinouts

| Mbed 2 | Mono Audio Amp | Speaker | Pin 2 on Pi | Pin 6 on Pi |
| :----: | :------------: | :-----: | :---------: | :---------: |
|  P18   |      IN+       |   nc    |     nc      |     nc      |
|  GND   |   PWR-, IN-    |   nc    |     nc      |     GND     |
|   nc   |      OUT+      |    +    |     nc      |     nc      |
|   nc   |      OUT-      |    -    |     nc      |     nc      |
|   nc   |      PWR+      |   nc    |     5V+     |     nc      |

## Left Side Sonar Sensor Pinouts

| Mbed 2 | Left HC-SR04 | Pin 2 on Pi | Pin 6 on Pi |
| :----: | :----------: | :---------: | :---------: |
|  GND   |     GND      |     nc      |     GND     |
|   nc   |     Vcc      |     5V+     |     nc      |
|   P6   |     Trig     |     nc      |     nc      |
|   P7   |     Echo     |     nc      |     nc      |

## Right Side Sonar Sensor Pinouts

| Mbed 2 | Right HC-SR04 | Pin 2 on Pi | Pin 6 on Pi |
| :----: | :-----------: | :---------: | :---------: |
|  GND   |      GND      |     nc      |     GND     |
|   nc   |      Vcc      |     5V+     |     nc      |
|  P12   |     Trig      |     nc      |     nc      |
|  P13   |     Echo      |     nc      |     nc      |

## Pi Camera Servo Motor

| Mbed 1 | Micro Servo SG90 | Pin 2 on Pi | Pin 6 on Pi |
| :----: | :--------------: | :---------: | :---------: |
|  GND   |      Brown       |     nc      |     GND     |
|   nc   |       Red        |     5V+     |     nc      |
|  P24   |      Orange      |     nc      |     nc      |

## Pi Camera Servo Mount

The pi camera servo mount was designed based off an existing servo mount but it was extend to include a semi-circle base that contained the pi camera mount on it. The mount was 3D printed at the Invention Studio in the MDCR. It was mounted to the microservo motor using a screw. The STereoLithography (STL) file and inventor file are included on the GitHub page.

<p align="center"><img width=50% src="build/images/3D print 1.jpg"></p>
<p align="center"><img width=50% src="build/images/mount.jpg"></p>

# Demo

[![RC Car Demo](https://img.youtube.com/vi/TS9khvXI--E/0.jpg)](https://www.youtube.com/watch?v=TS9khvXI--E "RC Car Demo")

# Presentation

[![RC Car Presentation](https://img.youtube.com/vi/KlX4RG750h4/0.jpg)](https://www.youtube.com/watch?v=KlX4RG750h4 "RC Car Presentation")

# Contributing

Feel free to fork over and utilize our code for future projects. Our goal was to utilize the material that we accumulated over the semester in our embedded systems class and combine the skills we learned into one project.

#### Team Members

- Nicole Komocsar
- Zarif Rahman
- Marcus Chan
- Alan Jin
