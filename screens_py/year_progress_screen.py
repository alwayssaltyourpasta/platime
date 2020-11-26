import main
from kivy.uix.screenmanager import Screen, ScreenManager


class YearProgress(Screen):
    pass

sm = ScreenManager()
sm.add_widget(YearProgress(name="year_progress"))