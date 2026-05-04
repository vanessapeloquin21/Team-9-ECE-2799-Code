import network
import time

ssid = '14.5Goulding1'
password = 'Wpirow27'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
wlan.config(pm=0xa11140)

# Wait for connection
while not wlan.isconnected():
    print("Connecting...")
    time.sleep(1)

print("Connected! IP:", wlan.ifconfig()[0])