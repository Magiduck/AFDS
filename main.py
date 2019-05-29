import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from plyer import call
from plyer import gps
from kivy.properties import StringProperty

import os.path


class TimerScreen(BoxLayout):

    def __init__(self, **kwargs):

        self.orientation = 'vertical'
        super(TimerScreen, self).__init__(**kwargs)
        self.countdown = Label(text='30', font_size=120, size_hint=(1, .75))
        self.ok_button = Button(text='I am okay', font_size=72, size_hint=(1, .25))
        self.ok_button.bind(on_press=self.cancel_timer)
        self.add_widget(self.countdown)
        self.add_widget(self.ok_button)
        self.count = 31
        gps.configure(on_location=self.on_location)
        self.gps_location = StringProperty()
        Clock.schedule_interval(self.timer, 1)

    def timer(self, dt):
        if self.count == 0:
            self.countdown.font_size = 48
            self.countdown.text = self.get_map_location()
            gps.stop()
            Clock.unschedule(self.timer)
            # call.makecall("+36306241796")
        else:
            self.alarm()
            self.count -= 1
            self.countdown.text = str(self.count)

    def cancel_timer(self, instance):
        Clock.unschedule(self.timer)
        self.countdown.font_size = 72
        self.countdown.text = "Cancelled the countdown!"

    def alarm(instance):
        if instance.count == 5:
            gps.start()
            final_sound = SoundLoader.load(os.path.join("Audio", "contacting_help.mp3"))
            if final_sound:
                final_sound.play()
        elif instance.count % 5 == 0:
            alarm_sound = SoundLoader.load(os.path.join("Audio", "alarm.mp3"))
            if alarm_sound:
                alarm_sound.play()

    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

    def get_map_location(self):
        lon = '0'
        lat = '0'
        for line in str(self.gps_location).split('\n'):
            if 'lon' in line:
                lon = line.split('=')[1]
            elif 'lat' in line:
                lat = line.split('=')[1]
        return "https://www.google.nl/maps/@"+lat+","+lon+",20z"


class AFDSApp(App):

    def build(self):
        return TimerScreen()


if __name__ == '__main__':
    AFDSApp().run()
