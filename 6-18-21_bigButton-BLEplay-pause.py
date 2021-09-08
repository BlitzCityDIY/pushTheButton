import time
import adafruit_ble
import board
from adafruit_debouncer import Debouncer
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
from adafruit_ble_apple_media import AppleMediaService
from digitalio import DigitalInOut, Direction, Pull

#  button pin
pin = DigitalInOut(board.D6)
pin.direction = Direction.INPUT
pin.pull = Pull.UP
big_button = Debouncer(pin)

#  BLE setup
radio = adafruit_ble.BLERadio()
a = SolicitServicesAdvertisement()
a.solicited_services.append(AppleMediaService)
radio.start_advertising(a)

while not radio.connected:
    pass

print("connected")

known_notifications = set()
button_state = False
i = 0
while radio.connected:
    
    #  found play/pause wasn't reliably working unless also recieving data from ams
    
    for connection in radio.connections:
        if not connection.paired:
            connection.pair()
            print("paired")
            time.sleep(3)
            ams = connection[AppleMediaService]
            print("App:", ams.player_name)
            print("Title:", ams.title)
            print("Album:", ams.album)
            print("Artist:", ams.artist)

        big_button.update()
        #ams = connection[AppleMediaService]

        if big_button.fell:
            print("App:", ams.player_name)
            print("Title:", ams.title)
            print("Album:", ams.album)
            print("Artist:", ams.artist)

            ams.toggle_play_pause()

print("disconnected")
