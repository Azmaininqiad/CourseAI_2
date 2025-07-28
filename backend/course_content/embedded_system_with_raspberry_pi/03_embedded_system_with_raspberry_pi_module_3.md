```markdown
# Module 3: Embedded System with Raspberry Pi - Interfacing with Sensors and Actuators

## Introduction  
Welcome to Module 3! In this module, you'll learn how Raspberry Pi interacts with the physical world through **sensors** (that detect environmental changes) and **actuators** (that create physical responses). By the end, you'll be able to:  
- Understand sensor/actuator communication protocols  
- Read data from digital/analog sensors  
- Control motors and LEDs programmatically  
- Build a basic environmental monitoring system  

---

## Topic 3.1: Sensor Fundamentals and GPIO Communication  

### What is a Sensor?  
Sensors convert physical phenomena (temperature, light, motion) into electrical signals. In embedded systems:  
- **Digital sensors** output discrete values (e.g., motion detected = HIGH)  
- **Analog sensors** output continuous voltage (requires ADC conversion)  

### Raspberry Pi GPIO Pins  
General Purpose Input/Output (GPIO) pins allow communication with hardware. Understanding pin numbering is critical for proper connections:  

![Raspberry Pi GPIO Pinout for Model A+](https://www.pi4j.com/1.2/images/j8header-photo-a-plus.png)  
*Figure: GPIO pin layout showing Broadcom (BCM) numbering standard*  

```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(14, GPIO.IN) # Set pin 14 as input
```

### Reading a Digital Sensor (Example: PIR Motion Sensor)  
1. **Hardware Setup**:  
   - PIR VCC → Pi 3.3V  
   - PIR GND → Pi GND  
   - PIR OUT → GPIO 14  

2. **Python Code**:  
```python
try:
    while True:
        motion = GPIO.input(14)
        if motion:
            print("Motion detected!")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
```

---

## Topic 3.2: Analog Sensors and ADC Conversion  

### Why ADC is Needed  
Raspberry Pi lacks native analog input. Use an **ADC (Analog-to-Digital Converter)** like MCP3008:  

### Reading Temperature (LM35 Analog Sensor)  
**Wiring**:  
- LM35 VCC → 3.3V  
- LM35 OUT → MCP3008 CH0  
- MCP3008 VDD → 3.3V, DGND → GND  

**Python Code (using `gpiozero`)**:  
```python
from gpiozero import MCP3008

temp_sensor = MCP3008(channel=0)
voltage = temp_sensor.value * 3.3
temp_c = voltage * 100  # LM35: 10mV per °C
print(f"Temperature: {temp_c:.2f}°C")
```

### 📺 Related Video: [Object Distance Calculation using Raspberry Pi and Ultrasonic sensor](https://www.youtube.com/watch?v=zFtCEIRpXwo)  
*Description: Demonstrates HC-SR04 ultrasonic sensor integration with Raspberry Pi for distance measurement and IoT data logging to ThingSpeak. Covers wiring, Python code, and real-time visualization.*

---

## Topic 3.3: Controlling Actuators with GPIO  

### Driving DC Motors  
Use an **H-Bridge (L298N)** to control motor direction/speed:  

**Wiring**:  
- L298N IN1 → GPIO 17, IN2 → GPIO 27  
- Motor Power → External 5V supply  

**Python Code for Bidirectional Control**:  
```python
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

# Rotate clockwise
GPIO.output(17, GPIO.HIGH)
GPIO.output(27, GPIO.LOW)

# Stop motor
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
```

### PWM for Speed Control  
```python
motor_pwm = GPIO.PWM(17, 100)  # 100Hz frequency
motor_pwm.start(50)  # 50% duty cycle
```

### Servo Motor Control  
```python
servo = GPIO.PWM(18, 50)  # 50Hz for servos
servo.start(0)

# Move to 90 degrees
duty_cycle = (90 / 18) + 2  # Convert angle to duty cycle %
servo.ChangeDutyCycle(duty_cycle)
```

---

## Project: Environmental Monitor System  
Combine sensors/actuators to build a system that:  
1. Reads temperature/humidity (DHT11)  
2. Triggers a fan (DC motor) if >30°C  
3. Alerts with LED when humidity <40%  

**Pseudocode Outline**:  
```python
while True:
    temp, humid = read_dht11()
    if temp > 30:
        activate_fan()
    if humid < 40:
        blink_warning_led()
```

---

## Key Takeaways  
- Digital sensors use binary states; analog sensors require ADC  
- GPIO pins enable hardware communication (configure as IN/OUT)  
- Motors need drivers (L298N) for sufficient current  
- PWM controls actuator speed/position  
- Sensor data can trigger actuator responses in automated systems  

---

## Practice Exercises  
1. Connect a button to GPIO 4. Write code to toggle an LED when pressed.  
2. Measure light intensity with an LDR. Convert reading to "Lux" using voltage division.  
3. Make a servo sweep 0°→180°→0° repeatedly.  
4. *Challenge*: Use a relay module to turn on a desk lamp via a mobile app (use Flask API).  

---

## References & Further Reading  
| Resource | Description |  
|----------|-------------|  
| [gpiozero Documentation](https://gpiozero.readthedocs.io) | Simplified GPIO control library |  
| [MCP3008 Datasheet](https://www.microchip.com/en-us/product/MCP3008) | ADC specifications |  
| *"Raspberry Pi Cookbook" by Simon Monk* | Chapter 10: Sensors & Actuators |  
| [Adafruit Learning System](https://learn.adafruit.com) | Sensor/actuator tutorials |  

## Visual Resources  
- **GPIO Pinout Diagram**:  
  ![Raspberry Pi GPIO Reference](https://www.pi4j.com/1.2/images/j8header-photo-a-plus.png)  
  Essential reference for sensor/actuator wiring configurations  

- **Sensor Integration Video**:  
  [Object Distance Calculation using Raspberry Pi and Ultrasonic sensor](https://www.youtube.com/watch?v=zFtCEIRpXwo)  
  Practical implementation guide for ultrasonic sensors with IoT integration  
```