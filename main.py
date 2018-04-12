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


class Main(wx.Frame):
    def __init__(self, parent, title, style):
        super(Main, self).__init__(parent, title=title, size=(wx.GetDisplaySize()))
        (self.display_length, self.display_height) = self.GetSize()
        self.pnl = wx.Panel(self)
        self.pnl.SetSize(self.GetSize())
        self.welcome_st()
        self.Move((0, 30))
        self.Show(True)
        self.price = 0.0
        self.amount = 0.0
        self.Maximize()
        self.filling = False

    def reset_panel(self):
        self.pnl.DestroyChildren()
        self.pnl.Destroy()
        self.pnl = wx.Panel(self)
        self.pnl.SetSize(self.GetSize())
        self.pnl.SetFocus()

    def welcome_st(self, event=None):

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
        self.pic1 = wx.StaticBitmap(self.pnl, -1, wx.Bitmap(pic), (0, 0))
        # self.pnl.Bind(wx.EVT_MOUSE_EVENTS, self.fill_st)
        # self.move_to_5_button = wx.Button(self, label="MOVE", pos=(0,0), size=(self.display_length, self.display_height))
        # self.Bind(wx.EVT_BUTTON, self.fill_st, self.move_to_5_button)

        GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=self.fill_st, bouncetime=500)

    def fill_st(self, event=None):
        GPIO.remove_event_detect(BUTTON)
        # self.reset_panel()
        print("I'm in fill_st")

        pic = wx.ImageFromBitmap(wx.Bitmap('5 Count up.png'))
        pic = pic.Scale(self.display_length, self.display_height, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self.pnl, -1, wx.Bitmap(pic), (0, 0))
        self.pic1.Hide()
        font = wx.Font(120, wx.MODERN, wx.NORMAL, wx.BOLD)
        self.ounces_text = wx.StaticText(self.pnl, pos=((self.display_length / 3) * 1.85, self.display_height / 5.2))
        self.price_text = wx.StaticText(self.pnl, pos=((self.display_length / 3) * 1.85, self.display_height / 2.3))
        self.ounces_text.SetForegroundColour(wx.Colour(255, 255, 255))
        self.price_text.SetForegroundColour(wx.Colour(255, 255, 255))
        self.ounces_text.SetFont(font)
        self.price_text.SetFont(font)
        self.ounces_text.SetLabelText("%05.2f" % self.amount)
        self.price_text.SetLabelText("%05.2f" % self.price)
        # self.ounces_text.Refresh()
        # self.price_text.Refresh()
        self.filling = True
        # self.pnl.Bind(wx.EVT_RIGHT_DOWN, self.fill)

        btn = wx.Button(self)
        self.Bind(wx.EVT_BUTTON, self.fill, btn)
        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, btn.GetId())
        self.stop_button = wx.Button(self, label="STOP", pos=(0, 0), size=(self.display_length, self.display_height))
        self.Bind(wx.EVT_BUTTON, self.stop_fill, self.stop_button)
        print('start')
        # while self.filling:
        #    if GPIO.input(BUTTON) == True:
        #        GPIO.output(RELAY, GPIO.HIGH)
        #        wx.PostEvent(self, evt)
        #        time.sleep(.3)
        try:
            while self.filling:
                if GPIO.input(BUTTON) == True:
                    GPIO.output(RELAY, GPIO.HIGH)
                    wx.PostEvent(self, evt)
                # time.sleep(.3)
                else:
                    print("I'm not pushed")
                    # GPIO.ouput(RELAY, GPIO.LOW)
                time.sleep(.3)
        finally:
            btn.Destroy()
        self.end_fill_st(self)

        # self.pnl.Bind(wx.EVT_KEY_DOWN, self.fill)
        # self.pnl.Bind(wx.EVT_KEY_DOWN, self.end_fill_st)

    def stop_fill(self, event):
        self.filling = False

    def fill(self, event=None):
        self.amount += 0.21
        self.price = self.amount / 10
        print("Ounces: %.2f Price: %.2f" % (self.amount, self.price))
        self.ounces_text.SetLabelText("%05.2f" % self.amount)
        self.price_text.SetLabelText("%05.2f" % self.price)
        # time.sleep(.5)

    def end_fill_st(self, event=None):
        self.stop_button.Destroy()
        print("I made it here")
        self.reset_panel()
        print("I'm in end_fill_st")
        pic = wx.ImageFromBitmap(wx.Bitmap('6 count stopped.png'))
        pic = pic.Scale(self.display_length, self.display_height, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self.pnl, -1, wx.Bitmap(pic), (0, 0))
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
        self.move_to_8_button = wx.Button(self, label="MOVE", pos=(0, 0),
                                          size=(self.display_length, self.display_height))
        self.Bind(wx.EVT_BUTTON, self.thank_you_st, self.move_to_8_button)

    def thank_you_st(self, event):
        self.move_to_8_button.Destroy()
        self.reset_panel()
        pic = wx.ImageFromBitmap(wx.Bitmap('8 thank you.png'))
        pic = pic.Scale(self.display_length, self.display_height, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self, -1, wx.Bitmap(pic), (0, 0))
        self.move_to_1_button = wx.Button(self, label="MOVE", pos=(0, 0),
                                          size=(self.display_length, self.display_height))
        self.Bind(wx.EVT_BUTTON, self.welcome_st, self.move_to_1_button)


if __name__ == '__main__':
    app = wx.App()
    Main(None, title='Tide Detergent Station', style=wx.NO_BORDER)
    app.MainLoop()