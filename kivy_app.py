import kivy
kivy.require('1.0.6')

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter


class PicturesApp(App):

    def build(self):
        return Button

    def on_pause(self):
        return True


if __name__ == '__main__':
    PicturesApp().run()