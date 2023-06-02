import machine
import time

LEFT_SENSOR_PIN = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
MIDDLE_SENSOR_PIN = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
RIGHT_SENSOR_PIN = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

def read_sensor(pin):
    # Set the pin to input mode
    pin.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
    
    # Wait for the sensor to settle
    time.sleep_ms(10)
    
    # Read the sensor value
    value = pin.value()
    
    # Return the value
    return value

# Initialize the PWM pins
pwm_pin1 = machine.Pin(9)
pwm1 = machine.PWM(pwm_pin1)

pwm_pin2 = machine.Pin(11)
pwm2 = machine.PWM(pwm_pin2)

# Set the PWM frequency
pwm1.freq(1000)
pwm2.freq(1000)

# Set the duty cycle to control the speed of the motors
pwm1.duty_u16(0)
pwm2.duty_u16(0)

# Define button pins
button_pin1 = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
button_pin2 = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_UP)

# Define the function to start the car
def start_car():
    pwm1.duty_u16(32768) # 50% duty cycle
    pwm2.duty_u16(32768) # 50% duty cycle

# Define the function to stop the car
def stop_car():
    pwm1.duty_u16(0)
    pwm2.duty_u16(0)

while True:
    # Wait for the button 21 to be pressed and the middle sensor to detect black to start the car
    while button_pin1.value() == 1 or middle_sensor_value == 1:
        middle_sensor_value = read_sensor(MIDDLE_SENSOR_PIN)

    # Start the car
    start_car()

    # Wait for the button 20 to be pressed to stop the car
    while button_pin2.value() == 1:
        # Read the sensor values while the car is running
        left_sensor_value = read_sensor(LEFT_SENSOR_PIN)
        middle_sensor_value = read_sensor(MIDDLE_SENSOR_PIN)
        right_sensor_value = read_sensor(RIGHT_SENSOR_PIN)

        print("Left sensor:", left_sensor_value)
        print("Middle sensor:", middle_sensor_value)
        print("Right sensor:", right_sensor_value)

        # If all sensors detect black, stop the car
        if left_sensor_value == 0 and middle_sensor_value == 0 and right_sensor_value == 0:
            stop_car()
            break

        # Adjust the motor speeds based on the sensor values
        if left_sensor_value == 0 and right_sensor_value == 1:
            # Turn left by stopping the left motor and setting the right motor to half speed
            pwm1.duty_u16(0)
            pwm2.duty_u16(int(32768 * 0.75))

            # Keep turning left until the middle sensor sees black
            while middle_sensor_value == 1:
                middle_sensor_value = read_sensor(MIDDLE_SENSOR_PIN)
        elif left_sensor_value == 1 and right_sensor_value == 0:
            # Turn right by stopping the right motor and setting the left motor to half speed
            pwm1.duty_u16(int(32768 * 0.75))
            pwm2.duty_u16(0)

            # Keep turning right until the middle sensor sees black
            while middle_sensor_value == 1:
                middle_sensor_value = read_sensor(MIDDLE_SENSOR_PIN)
        else:
            # Drive straight if both sensors are over a black surface or both are over a white surface
            pwm1.duty_u16(int(32768 * 0.75))
            pwm2.duty_u16(int(32768 * 0.75))

        # Wait for a short period of time before reading the sensors again
        time.sleep_ms(100)

    # Stop the car
    stop_car()