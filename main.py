import kivy

kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

count = 31


class TimerScreen(BoxLayout):

    def __init__(self, **kwargs):
        self.orientation = 'vertical'
        super(TimerScreen, self).__init__(**kwargs)
        self.countdown = Label(text='0', font_size=72, size_hint=(1, .75))
        self.ok_button = Button(text='I am okay', font_size=16, size_hint=(1, .25))
        self.ok_button.bind(on_press=self.cancelTimer)
        self.add_widget(self.countdown)
        self.add_widget(self.ok_button)
        Clock.schedule_interval(self.timer, 1)

    def timer(self, dt):
        global count
        if count == 0:
            Clock.unschedule(self.timer)
        else:
            self.alarm(self)
            count -= 1
            self.countdown.text = str(count)

    def cancelTimer(self, instance):
        Clock.unschedule(self.timer)
        self.countdown.text = "Cancelled the countdown!"

    def alarm(self, instance):
        global count
        if count == 5:
            final_sound = SoundLoader.load("Audio/contacting_help.mp3")
            if final_sound:
                final_sound.play()
        elif count % 5 == 0:
            alarm_sound = SoundLoader.load("Audio/alarm.mp3")
            if alarm_sound:
                alarm_sound.play()


class AFDSApp(App):

    def build(self):
        return TimerScreen()


if __name__ == '__main__':
    AFDSApp().run()
