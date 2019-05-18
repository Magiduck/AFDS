import kivy

kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class TimerScreen(BoxLayout):

    def __init__(self, **kwargs):
        self.orientation = 'vertical'
        super(TimerScreen, self).__init__(**kwargs)
        countdown = Label(text='30.0 seconds', font_size=72)
        ok_button = Button(text='I am okay', font_size=32)
        self.add_widget(countdown)
        self.add_widget(ok_button)


class AFDSApp(App):

    def build(self):
        return TimerScreen()


if __name__ == '__main__':
    AFDSApp().run()
