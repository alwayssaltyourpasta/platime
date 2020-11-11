import main
from kivy.uix.screenmanager import Screen, ScreenManager

class StatisticsScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(StatisticsScreen(name="statistics_screen"))