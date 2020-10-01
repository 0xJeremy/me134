from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

kit.servo[0].actuation_range = 270
kit.servo[1].actuation_range = 270
kit.servo[2].actuation_range = 270

kit.servo[0].set_pulse_width_range(500, 2500)
kit.servo[1].set_pulse_width_range(500, 2500)
kit.servo[2].set_pulse_width_range(500, 2500)

kit.servo[0].angle = 0
kit.servo[1].angle = 30
kit.servo[2].angle = 30
