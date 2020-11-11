import main
from kivy.uix.screenmanager import Screen, ScreenManager

class TodayScreen(Screen):
    def __init__(self, **kwargs):
        super(TodayScreen, self).__init__(**kwargs)
    def today_tasks(self):
        main.today(self.ids.today_list)

sm = ScreenManager()
sm.add_widget(TodayScreen(name="today_screen"))