import main
from kivy.uix.screenmanager import Screen, ScreenManager


class MonthProgress(Screen):
    def month_summary(self):
        main.summary(self, 30, self.ids.month_stats)

    def month_analysis(self):
        main.analysis(self, 30, self.ids.month_progress)


sm = ScreenManager()
sm.add_widget(MonthProgress(name="month_progress"))