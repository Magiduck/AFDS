import kivy

kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.clock import Clock

from plyer import gps
from plyer import accelerometer

import os.path
import math

# setup graphics
Config.set('graphics', 'resizable', 0)

# Graphics fix
Window.clearcolor = (0, 0, 0, 1.)

isTimerScreen = False

class AccelerometerScreen(Screen):
    # this is the main widget that contains the game
    def __init__(self, **kwargs):
        super(AccelerometerScreen, self).__init__(**kwargs)
        # setup accelerometer
        accelerometer.enable()
        self.label = ObjectProperty(None)
        self.labelf = ObjectProperty(None)
        self.labely = ObjectProperty(None)
        self.labelt = ObjectProperty(None)
        self.labelu = ObjectProperty(None)

        # add a label to advertise the blog
        self.x = 0
        self.y = 0
        self.z = 0
        self.total_accel = 0
        self.falling = False  # Initialisation
        self.hitGround = False
        self.low_measuring = 10
        self.high_measuring = 0
        self.timer_1 = 0
        self.timer_2 = 0

        # setup timer to update accelerometer
        # we want to regularly read the accelerometer
        Clock.schedule_interval(self.check_accel, 1.0 / 60.0)
        # these four functions use other plyer features to talk to the android api

    def check_accel(self, dt):  # Main program for the accelerometer
        # update label
        self.x = accelerometer.acceleration[0]  # Getting the information for the accelerometer
        self.y = accelerometer.acceleration[1]
        self.z = accelerometer.acceleration[2]
        self.total_accel = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)  # Calculating gravity
        txt = str(self.total_accel)
        self.ids.label.text = 'accelerometer: ' + txt

        if self.total_accel < 3.0 or self.falling is True:  # First fase falling
            self.falling = True
            self.ids.labelu.text = 'Fase:' + '1 Succeeded'
            if self.total_accel > 13.0 or self.hitGround is True:  # Second fase hitting the ground
                self.hitGround = True
                self.ids.labelu.text = 'Fase:' + '2 Succeeded'
                self.timer_1 = self.timer_1 + 1
                if self.timer_1 > 150 and 9.0 < self.total_accel < 11.0:  # Third fase sending a alarm
                    if self.timer_1 > 300:
                        self.hitGround = False
                        self.falling = False
                        self.timer_1 = 0
                        self.ids.labelt.text = 'Person has fallen:' + 'YES'
                        self.ids.labelu.text = 'Fase:' + '3 Succeeded'
                        global isTimerScreen
                        isTimerScreen = True
                        Clock.unschedule(self.check_accel)
                elif self.timer_1 > 150:  # Auto reset for third fase (for when there is still movement)
                    self.hitGround = False
                    self.falling = False
                    self.timer_1 = 0
                    self.ids.labelu.text = 'Fase:' + '3 Movement detected'
            elif 9.0 < self.total_accel < 11.0:  # Auto reset for when the fall is minor
                self.timer_2 = self.timer_2 + 1
                if self.timer_2 > 150:
                    self.hitGround = False
                    self.falling = False
                    self.timer_2 = 0
                    self.ids.labelu.text = 'Fase:' + '2 low readings'

        if self.total_accel < self.low_measuring:  # Measuring the low point of the falling
            self.low_measuring = self.total_accel
            self.ids.labely.text = 'measure low value:' + str(self.low_measuring)

        if self.total_accel > self.high_measuring:  # Measuring the High point of the falling
            self.high_measuring = self.total_accel
            self.ids.labelf.text = 'measure high value:' + str(self.high_measuring)


class TimerScreen(Screen):

    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)
        self.countdown = ObjectProperty(None)
        self.ok_button = ObjectProperty(None)
        self.count = 31
        gps.configure(on_location=self.on_location)
        self.gps_location = StringProperty()
        Clock.schedule_interval(self.timer, 1)

    def timer(self, dt):
        if isTimerScreen:
            if self.count == 0:
                self.ids.countdown.font_size = 48
                self.ids.countdown.text = self.get_map_location()
                gps.stop()
                Clock.unschedule(self.timer)
                # call.makecall("+36306241796")
            else:
                self.alarm()
                self.count -= 1
                self.ids.countdown.text = str(self.count)

    def cancel_timer(self):
        Clock.unschedule(self.timer)
        self.ids.countdown.font_size = 72
        self.ids.countdown.text = "Cancelled the countdown!"

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
        lon = ''
        lat = ''
        for line in str(self.gps_location).split('\n'):
            if 'lon' in line:
                lon = line.split('=')[1]
            elif 'lat' in line:
                lat = line.split('=')[1]
        return "https://www.google.nl/maps/@" + lat + "," + lon + ",20z"


class ScreenManagement(ScreenManager):

    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.current = 'Accelerometer'
        Clock.schedule_interval(self.check_if_change_screens, 0.5)

    def check_if_change_screens(self, dt):
        if isTimerScreen:
            self.current = 'Timer'


Builder.load_file("main.kv")


class AFDSApp(App):
    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    AFDSApp().run()
