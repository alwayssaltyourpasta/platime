import main
from kivy.uix.screenmanager import Screen, ScreenManager


class MonthProgress(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MonthProgress(name="month_progress"))