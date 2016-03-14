from kivy.uix.image import Image
from kivy.uix.behaviors.button import ButtonBehavior


class IconButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        self.allow_stretch = True
        super(IconButton, self).__init__(**kwargs)
        self.source_pressed = kwargs['source_pressed']
        self.callback = kwargs['callback']
        self.temp_source = None

    def on_press(self):
        self.temp_source = self.source
        self.source = self.source_pressed
        self.callback()

    def on_release(self):
        self.source = self.temp_source
