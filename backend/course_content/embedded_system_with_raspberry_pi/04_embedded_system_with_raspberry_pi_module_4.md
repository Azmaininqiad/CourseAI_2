```markdown
# Module 4: Embedded Systems with Raspberry Pi - Hands-on Applications

## Introduction
Welcome to Module 4! This module transforms your Raspberry Pi into an interactive embedded system. We'll explore GPIO control, sensor integration, and actuator management through practical projects. By the end, you'll build a weather station that reads environmental data and responds with physical outputs—blending software and hardware seamlessly. No prior electronics experience needed!

### 📺 Related Video: [Raspberry Pi Explained in 100 Seconds](https://www.youtube.com/watch?v=eZ74x6dVYes)  
*Description: What is a Raspberry Pi? Learn about all the parts and capabilities of the world's most popular tiny computer.*

**Learning Objectives**  
- Control GPIO pins programmatically  
- Interface with environmental sensors  
- Drive actuators using Pulse Width Modulation (PWM)  
- Process real-time sensor data  
- Build an integrated IoT project  

---

## Topic 4.1: Mastering GPIO Control

### What is GPIO?
General Purpose Input/Output (GPIO) pins allow your Raspberry Pi to interact with external components. These programmable pins can either:
- **Read signals** (Input mode: e.g., detect a button press)
- **Send signals** (Output mode: e.g., power an LED)

![GPIO Pinout Diagram](https://www.pi4j.com/1.2/images/j8header-photo-a-plus.png)  
*Fig 4.1: Standard 40-pin GPIO layout for Raspberry Pi (Model A+/B+, Pi 2/3/4)*

### Basic I/O Operations
Let's blink an LED using Python. Components needed:
- 1× LED
- 1× 220Ω resistor
- Breadboard and jumper wires

**Circuit Setup**:  
1. Connect LED cathode (short leg) to **GPIO 14** (Pin 8)  
2. Connect anode (long leg) to resistor  
3. Resistor to **3.3V** (Pin 1)  

**Python Code**:
```python
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
led_pin = 14

GPIO.setup(led_pin, GPIO.OUT)

try:
    while True:
        GPIO.output(led_pin, GPIO.HIGH)  # LED ON
        sleep(1)
        GPIO.output(led_pin, GPIO.LOW)   # LED OFF
        sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
```

**Code Explanation**:  
- `GPIO.HIGH` sends 3.3V to the pin  
- `GPIO.LOW` sets pin to 0V  
- `KeyboardInterrupt` ensures clean exit  

⚠️ **Caution**: Exceeding 3.3V or 50mA per pin may damage the Pi!

---

## Topic 4.2: Sensor Integration - DHT11

### How Digital Sensors Work
Sensors convert physical phenomena into electrical signals. The **DHT11** measures temperature and humidity using a capacitive humidity sensor and thermistor. Key specs:
- Temperature range: 0–50°C (±2°C accuracy)  
- Humidity range: 20–80% (±5%)  
- Digital signal output (avoids analog conversion)  

### Wiring Diagram
Connect DHT11 to Raspberry Pi:  
| DHT11 Pin | Raspberry Pi |  
|-----------|--------------|  
| VCC       | 3.3V (Pin 1) |  
| DATA      | GPIO 4 (Pin 7)|  
| GND       | GND (Pin 9)  |  

### Data Reading Code
```python
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 4

try:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print(f"Temp: {temperature}°C | Humidity: {humidity}%")
    else:
        print("Sensor failure. Check wiring!")
except Exception as e:
    print(f"Error: {str(e)}")
```

**Troubleshooting Tips**:  
- Use "sudo raspi-config" to enable I2C/SPI interfaces  
- Short wire runs (<20cm) reduce signal noise  

---

## Topic 4.3: Actuator Control with PWM

### Pulse Width Modulation Fundamentals
PWM simulates analog outputs by rapidly toggling digital pins. By varying the **duty cycle** (ON vs OFF time), we control power delivery:  
- 0% duty cycle = 0V  
- 100% duty cycle = 3.3V  

### Servo Motor Control
Components: SG90 Micro Servo (operates at 50Hz)  

**Wiring**:  
| Servo Wire | Raspberry Pi |  
|------------|--------------|  
| Brown (GND) | GND (Pin 14) |  
| Red (VCC)   | 5V (Pin 2)   |  
| Orange (SIG)| GPIO 18 (Pin 12)|  

**Python Code for Angle Control**:  
```python
import RPi.GPIO as GPIO
import time

servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz frequency

def set_angle(angle):
    duty_cycle = (angle / 18) + 2.5  # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)

pwm.start(0)  # Initialize at 0°
try:
    set_angle(0)    # Move to 0°
    set_angle(90)   # Move to 90°
    set_angle(180)  # Move to 180°
finally:
    pwm.stop()
    GPIO.cleanup()
```

### Practical Application: Automated Fan
Combine concepts to create a temperature-activated fan:  
1. Read temperature via DHT11  
2. If temp > 30°C, spin DC motor using PWM  
3. LED glows red when active  

---

## Key Takeaways
- 🛠️ **GPIO Pins**: Digital interfaces for hardware control  
- 📡 **Sensor Protocols**: Use libraries like Adafruit_DHT for complex sensors  
- ⚙️ **PWM**: Essential for proportional control of motors/LEDs  
- 🔁 **Real-time Systems**: Combine inputs and outputs for responsive behaviors  

---

## Practice Exercises
1. **LED Dimmer**: Create a script that gradually brightens/dims an LED using PWM  
2. **Smart Alert System**: Program a buzzer to beep when DHT11 detects humidity >70%  
3. **Challenge**: Build a sun-tracking system using photoresistors and a servo  

**Quiz**:  
1. What happens if you connect a 5V sensor directly to a Pi GPIO?  
2. Why is a resistor necessary for LEDs?  
3. How does PWM reduce power consumption vs constant voltage?  

---

## References & Further Reading
- **Books**:  
  - *Raspberry Pi Cookbook* by Simon Monk  
  - *Exploring Raspberry Pi* by Derek Molloy  
- **Datasheets**:  
  - [DHT11 Datasheet](https://cdn-shop.adafruit.com/datasheets/DHT11-chinese.pdf)  
  - [SG90 Servo Specifications](https://components101.com/motors/sg90-servo-motor)  
- **Tutorials**:  
  - Raspberry Pi Foundation [GPIO Tutorials](https://projects.raspberrypi.org/en/pathways/physical-computing)  
  - Adafruit [Learning System](https://learn.adafruit.com)  

## Visual Resources
### 🔍 Images
- **[GPIO Pinout Diagram](https://www.pi4j.com/1.2/images/j8header-photo-a-plus.png)**  
  Standard 40-pin layout for Raspberry Pi GPIO control  

### ▶️ Videos
- **[Raspberry Pi Explained in 100 Seconds](https://www.youtube.com/watch?v=eZ74x6dVYes)**  
  Quick overview of Raspberry Pi capabilities and components (Fireship)  

> *"Hardware teaches you patience. When it works—magic. When it doesn't—debugging is your new superpower."*  

Word count: 1495 words | Estimated reading: 12 minutes
```