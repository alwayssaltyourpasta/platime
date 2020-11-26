import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.progressbar import MDProgressBar
from kivy.utils import get_color_from_hex

class TodayProgress(Screen):
    def today_progress(self):
        self.ids.progress.add_widget(
            MDProgressBar(
                pos_hint={"center_x": 0.5, "center_y": 0.95},
                size_hint_x=0.5,
                value=50,
                color=get_color_from_hex('#e5e5e5')

            )
        )

sm = ScreenManager()
sm.add_widget(TodayProgress(name="today_progress"))