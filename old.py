# #!/usr/bin/env python3
import wx
# import images
import time
import threading
from threading import Thread
from multiprocessing.pool import ThreadPool
from wx.lib.pubsub import pub


import RPi.GPIO as GPIO

# GPIO PINS
# inputs
BUTTON = 40
PHOTO_TRANSISTOR = 37
# outputs
RELAY = 38
LED = 12
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)
GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(PHOTO_TRANSISTOR, GPIO.IN)
GPIO.setup(RELAY, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(RELAY, GPIO.LOW)
GPIO.output(LED, GPIO.HIGH)

FONT_SIZE = 57
OUNCE_HEIGHT = 4.8
PRICE_HEIGHT = 2.2


class Counter (Thread):
    def __init__(self, label1, label2, ounces):
        Thread.__init__(self)
        self.label1 = label1
        self.label2 = label2
        self.ounces = ounces
        self.filling = True

    def run(self):
        print("open relay")
        self.start_count(self.label1, self.label2)
        self.start_dispense()

    def stop(self):
        self.filling = False
        time.sleep(.5)
        return self.ounces

    def start_count(self, label1, label2):
        self.count_one(label1, label2)

    def count_one(self, label1, label2):
        self.ounces += .13
        # label1.SetLabelText("%05.2f" % self.ounces)
        wx.CallAfter(label1.SetLabelText, "%05.2f" % self.ounces)
        # label2.SetLabelText("%05.2f" % (self.ounces/10))
        wx.CallAfter(label2.SetLabelText, "%05.2f" % (self.ounces/10))
        time.sleep(.3)
        if self.filling:
            self.count_one(label1, label2)

    def start_dispense(self):
        self.dispense()

    def dispense(self):
        if self.filling:
            time.sleep(.5)
            self.dispense()
        else:
            print("close relay")


class Main(wx.Frame):
    def __init__(self, parent, title, style):
        super(Main, self).__init__(parent, title=title, size=(800, 480))
        (self.display_length, self.display_height) = self.GetSize()
        self.pnl = wx.Panel(self)
        self.pnl.SetSize(self.GetSize())
        self.welcome_st()
        self.Move((0, 30))
        self.Show(True)
        self.price = 0.0
        self.amount = 0.0
        # self.Maximize()
        self.filling = False
        self.counter = None

    def reset_panel(self):
        self.pnl.DestroyChildren()
        self.pnl.Destroy()
        self.pnl = wx.Panel(self)
        self.pnl.SetSize(self.GetSize())
        self.pnl.SetFocus()

    def reset_frame(self):
        self.DestroyChildren()
        self.pnl = wx.Panel(self)
        self.pnl.SetSize(self.GetSize())
        self.pnl.SetFocus()

    def welcome_st(self, event=None):
        self.amount = 0.0
        self.price = 0.0
        # self.reset_panel()
        self.reset_frame()
        print("I'm in welcome state")
        # self.bitmap1 = wx.StaticBitmap(self, -1, wx.Bitmap('1 welcome.png'), (0,0))
        pic = wx.ImageFromBitmap(wx.Bitmap('1 welcome.png'))
        pic = pic.Scale(self.display_length, self.display_height, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self.pnl, -1, wx.Bitmap(pic), (0, 0))

        self.move_to_2_button = wx.Button(self, label="MOVE", pos=(0, 0),
                                          size=(self.display_length, self.display_height))
        self.Bind(wx.EVT_BUTTON, self.insert_card_st, self.move_to_2_button)
        # pnl = wx.Panel(self)
        # self.pnl.Bind(wx.EVT_MOUSE_EVENTS, self.insert_card_st)
        self.pnl.SetFocus()

    def insert_card_st(self, event):
        self.move_to_2_button.Destroy()
        self.reset_panel()
        print("I'm in insert card state")
        pic = wx.ImageFromBitmap(wx.Bitmap('2 insert card.png'))
        pic = pic.Scale(self.display_length, self.display_height, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self.pnl, -1, wx.Bitmap(pic), (0, 0))

        # GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=self.place_bottle_instructions_st)
        # self.pnl.Bind(wx.EVT_MOUSE_EVENTS, self.place_bottle_instructions_st)
        self.move_to_3_button = wx.Button(self, label="MOVE", pos=(0, 0),
                                          size=(self.display_length, self.display_height))
        self.Bind(wx.EVT_BUTTON, self.place_bottle_instructions_st, self.move_to_3_button)

    def place_bottle_instructions_st(self, event):
        self.move_to_3_button.Destroy()
        self.reset_panel()
        print("I'm in bottle_instructions_st")
        # self.bitmap1 = wx.StaticBitmap(self, -1, wx.Bitmap('3 place bottle.png'), (0,0))
        pic = wx.ImageFromBitmap(wx.Bitmap('3 place bottle.png'))
        pic = pic.Scale(self.display_length, self.display_height, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self.pnl, -1, wx.Bitmap(pic), (0, 0))
        # self.pnl.Bind(wx.EVT_MOUSE_EVENTS, self.fill_instructions_st)
        self.move_to_4_button = wx.Button(self, label="MOVE", pos=(0, 0),
                                          size=(self.display_length, self.display_height))
        self.Bind(wx.EVT_BUTTON, self.fill_instructions_st, self.move_to_4_button)

    def fill_instructions_st(self, event):
        self.move_to_4_button.Destroy()
        self.reset_panel()
        print("I'm in fill_instructions_st")
        # self.bitmap1 = wx.StaticBitmap(self, -1, wx.Bitmap('3 place bottle.png'), (0,0))
        pic = wx.ImageFromBitmap(wx.Bitmap('4 Fill instructions.png'))
        pic = pic.Scale(self.display_length, self.display_height, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self.pnl, -1, wx.Bitmap(pic), (0, 0))
        # self.pnl.Bind(wx.EVT_MOUSE_EVENTS, self.fill_st)
        self.move_to_5_button = wx.Button(self, label="MOVE", pos=(0, 0), size=(self.display_length, self.display_height))
        self.Bind(wx.EVT_BUTTON, self.fill_st, self.move_to_5_button)

        # GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=self.fill_st, bouncetime=500)

    def fill_st(self, event=None):
        # GPIO.remove_event_detect(BUTTON)
        self.move_to_5_button.Destroy()
        self.reset_panel()
        print("I'm in fill_st")

        pic = wx.ImageFromBitmap(wx.Bitmap('5 Count up.png'))
        pic = pic.Scale(self.display_length, self.display_height, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self.pnl, -1, wx.Bitmap(pic), (0, 0))
        # self.pic1.Hide()
        font = wx.Font(FONT_SIZE, wx.MODERN, wx.NORMAL, wx.BOLD)
        self.ounces_text = wx.StaticText(self.pnl, pos=((self.display_length / 3) * 1.85, self.display_height / OUNCE_HEIGHT))
        self.price_text = wx.StaticText(self.pnl, pos=((self.display_length / 3) * 1.85, self.display_height / PRICE_HEIGHT))
        self.ounces_text.SetForegroundColour(wx.Colour(255, 255, 255))
        self.price_text.SetForegroundColour(wx.Colour(255, 255, 255))
        self.ounces_text.SetFont(font)
        self.price_text.SetFont(font)
        self.ounces_text.SetLabelText("%05.2f" % self.amount)
        self.price_text.SetLabelText("%05.2f" % self.price)

        print('start')

        # self.pnl.Bind(wx.EVT_KEY_DOWN, self.stop_fill)
        # btn = wx.Button(self)
        # self.Bind(wx.EVT_BUTTON, self.fill, btn)
        # evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, btn.GetId())
        # self.filling = True
        # while self.filling:
        #     if True:
        #         time.sleep(1)
        #         wx.PostEvent(self, evt)
        #         # wx.CallLater(1000, wx.PostEvent, self, evt)
        #         # wx.QueueEvent(self.pnl, evt)
        #
        # self.end_fill_st()


        self.filling = True
        self.counter = Counter(self.ounces_text, self.price_text, self.amount)
        self.counter.start()
        self.stop_button = wx.Button(self, label="STOP", pos=(0, 0), size=(self.display_length, self.display_height))
        self.Bind(wx.EVT_BUTTON, self.end_fill_st, self.stop_button)

        # GPIO.add_event_detect(BUTTON, GPIO.BOTH, callback=toggle_fill, bouncetime=500)
        btn = wx.Button(self)
        self.Bind(wx.EVT_BUTTON, self.toggle_fill, btn)
        self.evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, btn.GetId())
        GPIO.add_event_detect(BUTTON, GPIO.BOTH, callback=self.toggle_event, bouncetime=500)
        self.pnl.Bind(wx.EVT_KEY_DOWN, self.toggle_fill)

        # while self.filling:
        #    if GPIO.input(BUTTON) == True:
        #        GPIO.output(RELAY, GPIO.HIGH)
        #        wx.PostEvent(self, evt)
        #        time.sleep(.3)

        # while self.filling:
        # for i in range(10):
            # if GPIO.input(BUTTON) == True:
            # if (1==1):
                # GPIO.output(RELAY, GPIO.HIGH)
            # wx.PostEvent(self, evt)
            # time.sleep(1)
            # else:cd Docum
            #     print("I'm not pushed")
            #     # GPIO.ouput(RELAY, GPIO.LOW)
        #self.end_fill_st()

        # self.pnl.Bind(wx.EVT_KEY_DOWN, self.fill)
        # self.pnl.Bind(wx.EVT_KEY_DOWN, self.end_fill_st)

    def toggle_event(self, event):
        wx.PostEvent(self, self.evt)

    def fill(self, event=None):
        self.amount += 0.21
        self.price = self.amount / 10
        print("Ounces: %.2f Price: %.2f" % (self.amount, self.price))
        self.ounces_text.SetLabelText("%05.2f" % self.amount)
        self.price_text.SetLabelText("%05.2f" % self.price)
        # wx.CallAfter(self.ounces_text.SetLabelText, "%05.2f" % self.amount)
        # wx.CallAfter(self.price_text.SetLabelText, "%05.2f" % self.price)
        # time.sleep(.5)

    def stop_fill(self, event):
        self.filling = False

    def toggle_fill(self, event=None):
        if self.filling:
            self.amount = self.counter.stop()
            self.filling = False
        else:
            self.counter = Counter(self.ounces_text, self.price_text, self.amount)
            self.counter.start()
            self.filling = True

    def end_fill_st(self, event=None):
        GPIO.remove_event_detect(BUTTON)
        time.sleep(.3)
        if self.filling:
            self.toggle_fill()
            time.sleep(.5)
        self.stop_button.Destroy()
        self.reset_panel()
        print("I made it here")
        print("I'm in end_fill_st")
        font = wx.Font(FONT_SIZE, wx.MODERN, wx.NORMAL, wx.BOLD)
        pic = wx.ImageFromBitmap(wx.Bitmap('6 count stopped.png'))
        pic = pic.Scale(self.display_length, self.display_height, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self.pnl, -1, wx.Bitmap(pic), (0, 0))
        self.ounces_text = wx.StaticText(self.pnl, pos=((self.display_length / 3) * 1.85, self.display_height / OUNCE_HEIGHT))
        self.price_text = wx.StaticText(self.pnl, pos=((self.display_length / 3) * 1.85, self.display_height / PRICE_HEIGHT))
        self.ounces_text.SetForegroundColour(wx.Colour(255, 255, 255))
        self.price_text.SetForegroundColour(wx.Colour(255, 255, 255))
        self.ounces_text.SetFont(font)
        self.price_text.SetFont(font)
        self.ounces_text.SetLabelText("%05.2f" % self.amount)
        self.price_text.SetLabelText("%05.2f" % (self.amount/10))
        print("And I made it here")
        self.move_to_7_button = wx.Button(self, label="MOVE", pos=(0, 0),
                                          size=(self.display_length, self.display_height))
        self.Bind(wx.EVT_BUTTON, self.receipt_st, self.move_to_7_button)
        print("And done")

    def receipt_st(self, event):
        print("Made it to receipt state")
        self.move_to_7_button.Destroy()
        self.reset_panel()
        print("I'm in receipt_st")
        pic = wx.ImageFromBitmap(wx.Bitmap('7 receipt.png'))
        pic = pic.Scale(self.display_length, self.display_height, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self.pnl, -1, wx.Bitmap(pic), (0, 0))
        font = wx.Font(FONT_SIZE, wx.MODERN, wx.NORMAL, wx.BOLD)
        self.ounces_text = wx.StaticText(self.pnl, pos=((self.display_length / 3) * 1.85, self.display_height / OUNCE_HEIGHT))
        self.price_text = wx.StaticText(self.pnl, pos=((self.display_length / 3) * 1.85, self.display_height / PRICE_HEIGHT))
        self.ounces_text.SetForegroundColour(wx.Colour(255, 255, 255))
        self.price_text.SetForegroundColour(wx.Colour(255, 255, 255))
        self.ounces_text.SetFont(font)
        self.price_text.SetFont(font)
        self.ounces_text.SetLabelText("%05.2f" % self.amount)
        self.price_text.SetLabelText("%05.2f" % (self.amount / 10))
        self.move_to_8_button = wx.Button(self, label="MOVE", pos=(0, 0), size=(self.display_length, self.display_height))
        self.Bind(wx.EVT_BUTTON, self.thank_you_st, self.move_to_8_button)

    def thank_you_st(self, event):
        # self.move_to_8_button.Destroy()
        self.reset_frame()
        pic = wx.ImageFromBitmap(wx.Bitmap('8 thank you.png'))
        pic = pic.Scale(self.display_length, self.display_height, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self.pnl, -1, wx.Bitmap(pic), (0, 0))
        self.move_to_1_button = wx.Button(self, label="MOVE", pos=(0, 0),
                                          size=(self.display_length, self.display_height))
        self.Bind(wx.EVT_BUTTON, self.welcome_st, self.move_to_1_button)


if __name__ == '__main__':
    app = wx.App()
    Main(None, title='Tide Detergent Station', style=wx.NO_BORDER)
    app.MainLoop()