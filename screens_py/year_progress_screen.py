import main
from kivy.uix.screenmanager import Screen, ScreenManager


class YearProgress(Screen):
    def year_summary(self):
        main.summary(self, 365, self.ids.year_stats)

    def year_analysis(self):
        main.analysis(self, 365, self.ids.year_progress)


sm = ScreenManager()
sm.add_widget(YearProgress(name="year_progress"))