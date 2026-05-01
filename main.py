from machine import Pin, I2C
from mpu6050 import MPU6050
from ssd1306 import SSD1306_I2C
import time
import math

# Change pins if needed
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq = 400000)
oled = SSD1306_I2C(128, 32, i2c)
sensor = MPU6050(i2c)
print(i2c.scan())

#LED Pins
#redLED = Pin(16, Pin.OUT)
#yellowLED = Pin(17, Pin.OUT)
#greenLED = Pin(18, Pin.OUT)

#Specific Settings
THRESHOLD = 0.5  
max_force = 0.0
history = []
accel = sensor.get_values()
#btn = Pin(28, Pin.IN, Pin.PULL_UP)

prev_x = 0
prev_y = 0
prev_z = 0


def update_screen(current, peak, history_list):
    oled.fill(0)
    oled.text("PUNCH TRACKER", 0, 0)
    oled.hline(0, 8, 128, 1)
    oled.text(f"NOW:  {current:.2f} ", 5, 10)
    oled.text(f"BEST: {peak:.2f} ", 5, 18)
    oled.text("HISTORY: ", 3, 35)
    for i, p in enumerate(history_list[-3:]):
        oled.text(f"{p:.1f}", 5 + (i * 40), 35)
    oled.show()

print("-" * 30)
print("SYSTEM ACTIVE: Terminal Logging Enabled")
print("Using X + Y + Z acceleration")
print("-" * 30)
#redLED.value(1)
#yellowLED.value(1)
#greenLED.value(1)
#time.sleep(5)
#redLED.value(0)
#yellowLED.value(0)
#greenLED.value(0)
update_screen(0.0, 0.0, [])

while True:
  #if btn.value() == 0:
   #   max_force = 0.0
    #  history = []
    #  print("\n[SYSTEM] Records cleared by user.")
    #  update_screen(0.0, 0.0, [])
      #greenLED.value(1)
      #time.sleep(10)
      #greenLED.value(0)
    #  time.sleep(0.3)
    
  accel = sensor.get_values()
  
  #with open('data.txt', 'w') as f:
  #  f.write(str(accel) + "\n")

  ax = accel['AcX'] / 16384.0
  ay = accel['AcY'] / 16384.0
  az = accel['AcZ'] / 16384.0

  dx = ax - prev_x
  dy = ay - prev_y
  dz = az - prev_z

  current_g = math.sqrt(dx*dx + dy*dy + dz*dz)

  prev_x = ax
  prev_y = ay
  prev_z = az

  if current_g > THRESHOLD:
      start_time = time.ticks_ms()
      local_peak = current_g
      while time.ticks_diff(time.ticks_ms(), start_time) < 150:
            raw = sensor.get_values()
            ax = raw['AcX'] / 16384.0
            ay = raw['AcY'] / 16384.0
            az = raw['AcZ'] / 16384.0
            val = math.sqrt(ax*ax + ay*ay + az*az)
        
            if val > local_peak: 
                local_peak = val  
              
   #   if local_peak < 0.8:
         # color = "Red (Light)"
         # redLED.value(1)
          #time.sleep(10)
          #redLED.value(0)
     # elif local_peak < 1.5:
         # color = "Yellow (Medium)"
         # yellowLED.value(1)
         # time.sleep(10)
         # yellowLED.value(0)
    #  else:
         # color = "Green (Heavy)"
        #  greenLED.value(1)
       #   time.sleep(10)
        #  greenLED.value(0)
              
      history.append(local_peak) 
      if local_peak > max_force:
          max_force = local_peak
          print(f"*** NEW PERSONAL BEST: {max_force}  ***")
      else:
          update_screen(0.0, max_force, history)
          time.sleep(0.05)
    
        # Terminal Output
      print(f"Punch Detected | Force: {local_peak:.2f} ")
    
      update_screen(local_peak, max_force, history)
      #redLED.value(0)
      #yellowLED.value(0)
      #greenLED.value(0)
      #time.sleep(0.05)
        