from guizero import *
from itertools import count
import time
from threading import Thread
# import RPi.GPIO as GPIO

WIDTH = 800
HEIGHT = 480
background = None

# # GPIO PINS
# # inputs
# BUTTON = 40
# PHOTO_TRANSISTOR = 37
# # outputs
# RELAY = 38
# LED = 12
# GPIO.cleanup()
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(True)
# GPIO.setup(BUTTON, GPIO.IN)
# GPIO.setup(PHOTO_TRANSISTOR, GPIO.IN)
# GPIO.setup(RELAY, GPIO.OUT)
# GPIO.setup(LED, GPIO.OUT)
# GPIO.output(RELAY, GPIO.LOW)
# GPIO.output(LED, GPIO.HIGH)


class Counter (Thread):
    def __init__(self, label1, label2, ounces):
        Thread.__init__(self)
        self.label1 = label1
        self.label2 = label2
        self.ounces = ounces
        self.filling = True

    def run(self):
        self.start_count(self.label1, self.label2)

    def stop(self):
        self.filling = False
        return self.ounces

    def start_count(self, label1, label2):
        self.count_one(label1, label2)

    def count_one(self, label1, label2):
        self.ounces += .13
        label1.value = "%05.2f" % self.ounces
        label2.value = "%05.2f" % (self.ounces/10)
        time.sleep(.2)
        if self.filling:
            self.count_one(label1, label2)


class TideDispense:
    def __init__(self):
        self.background = None
        self.app = App("Tide Despenser", width=WIDTH, height=HEIGHT, layout="grid")
        self.ounces = 0.0
        self.price_per_ounce = .11
        self.filling = False
        self.box = None
        self.price_text = None
        self.ounces_text = None
        self.fill_state = False
        self.counter = None

    def welcome(self):
        self.background = Picture(self.app, image="1 welcome.png")
        self.background.width = WIDTH
        self.background.height = HEIGHT
        self.background.when_clicked = self.insert_card

    def insert_card(self):
        self.background.destroy()
        self.background = Picture(self.app, image="2 insert card.png")
        self.background.width = WIDTH
        self.background.height = HEIGHT
        self.background.when_clicked = self.place_bottle

    def place_bottle(self):
        self.background.destroy()
        self.background = Picture(self.app, image="3 place bottle.png")
        self.background.width = WIDTH
        self.background.height = HEIGHT
        self.background.when_clicked = self.fill_instructions

    def fill_instructions(self):
        self.background.destroy()
        self.background = Picture(self.app, image="4 Fill instructions.png")
        self.background.width = WIDTH
        self.background.height = HEIGHT
        self.background.when_clicked = self.fill
        # GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=self.fill_st, bouncetime=500)

    def fill(self):
        # GPIO.remove_event_detect(BUTTON)

        # Background
        # self.background.destroy()
        self.background = Picture(self.app, image="5 Count up.png", grid=[0, 0])
        self.background.width = WIDTH
        self.background.height = HEIGHT
        self.box = Box(self.app, grid=[0, 0], layout="grid")

        # Text
        self.ounces_text = Text(self.box, text="%05.2f" % self.ounces, size=120, grid=[10, 10])
        self.price_text = Text(self.box, text="%05.2f" % (self.ounces * self.price_per_ounce), size=120, grid=[10, 5])
        self.price_text.text_color = "white"
        self.ounces_text.text_color = "white"
        self.price_text.bg = "#EF5026"
        self.ounces_text.bg = "#EF5026"

        self.background.when_clicked = self.toggle_fill
        self.background.when_key_pressed = self.end_fill
        self.filling = True
        self.counter = Counter(self.ounces_text, self.price_text, self.ounces)
        self.counter.start()



    def end_fill(self):
        self.fill_state = False

    def toggle_fill(self):
        if self.filling:
            self.ounces = self.counter.stop()
            self.filling = False
        else:
            self.counter = Counter(self.ounces_text, self.price_text, self.ounces)
            self.counter.start()
            self.filling = True

    def run(self):
        self.fill()
        self.app.display()





if __name__ == '__main__':
    app = TideDispense()
    app.run()
