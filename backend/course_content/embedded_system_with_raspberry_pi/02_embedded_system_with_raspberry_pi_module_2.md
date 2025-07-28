```markdown
# Module 2: Raspberry Pi Hardware Interfaces and GPIO Programming

## Introduction  
Welcome to Module 2! Here, we dive into Raspberry Pi's hardware capabilities. You'll learn how to interact with sensors, LEDs, and other components using GPIO (General Purpose Input/Output) pins. By the end, you'll build a light-sensing alarm system ⚡. No prior hardware experience needed!

### 📺 Related Video: [Raspberry Pi Explained in 100 Seconds](https://www.youtube.com/watch?v=eZ74x6dVYes)  
*Description: What is a Raspberry Pi? Learn about all the parts and capabilities of the world's most popular tiny computer in this quick overview.*

---

## Topic 2.1: Anatomy of Raspberry Pi GPIO Pins  
### What is GPIO?  
GPIO pins allow your Pi to communicate with external hardware. Unlike dedicated ports (USB/HDMI), they’re programmable "blank slates."  

### Pin Layout Breakdown  
- **40-pin header**: Standard on Pi 3/4/Zero (26 pins on older models)  
- **Pin types**:  
  - Power pins (3.3V, 5V, Ground)  
  - Digital I/O (programmable for input/output)  
  - Specialized pins (I²C, SPI, UART for sensors)  

![Labeled GPIO diagram highlighting pin functions](https://www.pi4j.com/1.2/images/j8header-photo-a-plus.png)  

⚠️ **Critical Safety Rule**:  
> Never connect >3.3V directly to GPIO! Use level shifters for 5V components.  

---

## Topic 2.2: Circuit Fundamentals for Embedded Systems  
### Ohm’s Law Simplified  
```python
# Voltage (V) = Current (I) × Resistance (R)
# Example: Calculate resistor for a 2V LED at 0.02A
resistance = (3.3 - 2) / 0.02  # Result: 65Ω
```

### Building Your First Circuit  
**Components needed**:  
- LED (Light Emitting Diode)  
- 220Ω resistor (protects LED)  
- Jumper wires  

**Wiring Steps**:  
1. Connect Pi’s **GPIO17** → resistor → LED’s anode (+)  
2. Connect LED’s cathode (-) → Pi’s **GND** pin  

---

## Topic 2.3: Python GPIO Control (Hands-On Project)  
### Blink an LED with Code  
```python
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbers
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED ON
        sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)   # LED OFF
        sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()  # Reset GPIO states
```
**Run it**:  
```bash
python3 blink.py  # Press Ctrl+C to exit
```

### Add a Light Sensor (LDR)  
**Circuit Upgrade**:  
- Connect LDR between **3.3V** and **GPIO2**  
- Add 10kΩ resistor between **GPIO2** and **GND**  

**Detect Darkness**:  
```python
LDR_PIN = 2
GPIO.setup(LDR_PIN, GPIO.IN)

if GPIO.input(LDR_PIN) == GPIO.LOW:
    print("Dark! Triggering alert...")
```

---

## Key Takeaways  
✅ GPIO provides programmable hardware control  
✅ Always use resistors to limit current  
✅ `GPIO.HIGH`/`GPIO.LOW` control digital outputs  
✅ Sensors convert real-world data (e.g., light) to signals  

---

## Practice Exercises  
1. **Debugging**: The LED isn’t lighting. List 3 possible causes.  
2. **Modify Code**: Change the blink pattern to SOS Morse code (···−−−···).  
3. **Challenge**: Add a button to turn the LED on only when pressed.  

*Sample Solution for Exercise 2*:  
```python
# SOS: 3 short, 3 long, 3 short
def sos():
    for _ in range(3): blink(0.5)
    for _ in range(3): blink(1.5)
    for _ in range(3): blink(0.5)
```

---

## Visual Resources  
### 📺 Featured Video  
- **[Raspberry Pi Explained in 100 Seconds](https://www.youtube.com/watch?v=eZ74x6dVYes)**  
  - *Channel*: Fireship  
  - *Description*: Quick overview of Raspberry Pi hardware capabilities and components.  

### 📷 Essential Image  
- **[GPIO Pin Diagram](https://www.pi4j.com/1.2/images/j8header-photo-a-plus.png)**  
  - Detailed labeling of 40-pin header functions for hardware interfacing.  

## References & Further Reading  
- **[Official GPIO Documentation](https://www.raspberrypi.com/documentation/computers/os.html#gpio-and-the-40-pin-header)**  
- *Book*: "Raspberry Pi Cookbook" by Simon Monk (O’Reilly)  
- **Simulator**: Experiment virtually at [Wokwi Raspberry Pi Simulator](https://wokwi.com/projects/new/raspberry-pi)  

> 💡 **Pro Tip**: Always run `GPIO.cleanup()` to prevent damage between projects!
```