Enhanced markdown content for 05_embedded_system_with_raspberry_pi_module_5.md  

```markdown
# Module 5: Embedded System Development with Raspberry Pi  
**Difficulty Level**: Beginner  
**Estimated Reading Time**: 10-12 minutes  

## Introduction  
Welcome to Module 5! Here, we'll transform your Raspberry Pi into an embedded system powerhouse. You'll learn to interface with real-world components through GPIO pins, read sensor data, control actuators, and build a complete mini-project. By the end, you'll understand how to create responsive embedded systems that interact with their environment.  

---  

## Topic 5.1: GPIO Fundamentals and Digital I/O  

### What is GPIO?  
General Purpose Input/Output (GPIO) pins allow your Raspberry Pi to communicate with external electronics. These programmable pins can read signals (Input) or send control signals (Output).  

**Key Concepts**:  
- **Voltage Levels**: Raspberry Pi uses 3.3V logic (HIGH=3.3V, LOW=0V).  
- **Pin Identification**:  
  - Physical Pins: Numbered 1-40 (physical layout).  
  - BCM Pins: Broadcom SOC channel numbers (software addressing).  
  ![GPIO Pinout Diagram](https://www.pi4j.com/1.2/images/j8header-photo-a-plus.png)  
  *Figure: Raspberry Pi GPIO pin mapping (BCM vs Physical numbering)*  
- **Current Limits**: Max 16mA per pin; 50mA total across all pins.  

### Setting Up GPIO Control  
We'll use Python's `RPi.GPIO` library. First, install it:  
```bash  
sudo apt update && sudo apt install python3-rpi.gpio  
```  

#### Blinking LED Example  
**Components Needed**:  
- LED (any color)  
- 220Ω resistor  
- Jumper wires  

**Circuit Setup**:  
1. Connect LED cathode (short leg) to GPIO pin 14 (BCM).  
2. Connect anode (long leg) to resistor.  
3. Connect resistor to ground (GND).  

**Code** (`blink_led.py`):  
```python  
import RPi.GPIO as GPIO  
import time  

GPIO.setmode(GPIO.BCM)  # Use BCM numbering  
led_pin = 14  
GPIO.setup(led_pin, GPIO.OUT)  

try:  
    while True:  
        GPIO.output(led_pin, GPIO.HIGH)  # LED ON  
        time.sleep(1)  
        GPIO.output(led_pin, GPIO.LOW)   # LED OFF  
        time.sleep(1)  
except KeyboardInterrupt:  
    GPIO.cleanup()  # Reset GPIO  
```  
Run with: `python3 blink_led.py`  

---  

## Topic 5.2: Sensor Interfacing and Analog Input  

### Reading Digital Sensors  
Digital sensors output HIGH/LOW signals. We'll use a PIR motion sensor:  

**Wiring**:  
- VCC → 5V Pin (Physical pin 2)  
- OUT → GPIO 4 (BCM)  
- GND → Ground  

**Code** (`motion_detector.py`):  
```python  
sensor_pin = 4  
GPIO.setup(sensor_pin, GPIO.IN)  

try:  
    while True:  
        if GPIO.input(sensor_pin):  
            print("Motion detected!")  
        else:  
            print("No motion")  
        time.sleep(0.5)  
except KeyboardInterrupt:  
    GPIO.cleanup()  
```  

### Handling Analog Sensors  
Raspberry Pi lacks analog pins! Use an **ADC (Analog-to-Digital Converter)** like the MCP3008:  

**Wiring MCP3008**:  
- VDD → 3.3V  
- VREF → 3.3V  
- AGND → GND  
- CLK → GPIO 11 (BCM)  
- DOUT → GPIO 9  
- DIN → GPIO 10  
- CS → GPIO 8  

**Reading a Potentiometer**:  
```python  
import busio  
import digitalio  
import adafruit_mcp3xxx.mcp3008 as MCP  
from adafruit_mcp3xxx.analog_in import AnalogIn  

spi = busio.SPI(clock=11, MISO=9, MOSI=10)  
cs = digitalio.DigitalInOut(8)  
mcp = MCP.MCP3008(spi, cs)  
pot_channel = AnalogIn(mcp, MCP.P0)  

print(f"Voltage: {pot_channel.voltage:.2f}V")  
```  

---  

## Topic 5.3: Building a Smart Lighting System  
Let's combine concepts into a project that turns lights ON when motion is detected at night.  

**Components**:  
- PIR Motion Sensor  
- LDR (Light Dependent Resistor)  
- LED Strip (via relay module)  
- MCP3008 ADC  

### Step-by-Step Guide  
1. **Circuit Setup**:  
   - Connect PIR to GPIO 4 (digital input).  
   - Connect LDR to MCP3008 CH0 (analog input).  
   - Connect relay control pin to GPIO 17.  

2. **Code Logic**:  
```python  
ldr_channel = AnalogIn(mcp, MCP.P0)  
relay_pin = 17  
GPIO.setup(relay_pin, GPIO.OUT)  

while True:  
    light_level = ldr_channel.value  # 0-1023 (dark to bright)  
    motion = GPIO.input(sensor_pin)  
    
    if motion and light_level < 300:  # Dark environment  
        GPIO.output(relay_pin, GPIO.HIGH)  
    else:  
        GPIO.output(relay_pin, GPIO.LOW)  
    
    time.sleep(1)  
```  

3. **Testing**:  
   - Cover LDR to simulate darkness.  
   - Wave hand near PIR sensor.  
   - Observe LED strip turning ON/OFF automatically.  

---  

## Key Takeaways  
- GPIO pins enable hardware interaction using voltage states.  
- Digital sensors provide simple on/off signals, while analog sensors require ADCs.  
- Combining inputs (e.g., motion + light) creates context-aware systems.  
- Always handle GPIO cleanup to prevent pin state conflicts.  

---  

## Practice Exercises  
1. Modify the LED blink code to create an SOS pattern (···−−−···).  
2. Connect a button to turn the LED on only while pressed.  
3. Add serial output to the smart lighting system to log motion/light levels.  
4. **Challenge**: Use PWM to fade an LED based on potentiometer values.  

---  

## Visual Resources  
- ![GPIO Pinout Diagram](https://www.pi4j.com/1.2/images/j8header-photo-a-plus.png)  
  *Reference: Raspberry Pi GPIO pin mapping (BCM vs Physical numbering)*  

## References & Further Reading  
- **Books**:  
  - *Exploring Raspberry Pi* by Derek Molloy  
  - *Practical Electronics for Inventors* by Paul Scherz  
- **Links**:  
  - [RPi GPIO Documentation](https://www.raspberrypi.com/documentation/computers/os.html#gpio)  
  - [MCP3008 Datasheet](https://www.microchip.com/en-us/product/MCP3008)  
- **Kits**:  
  - SunFounder Raspberry Pi Starter Kit  
  - CanaKit Raspberry Pi Super Kit  

> "Hardware is just software crystallized early." – Alan Kay  
```