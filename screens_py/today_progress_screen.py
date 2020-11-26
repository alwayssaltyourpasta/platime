import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.progressbar import MDProgressBar
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDRoundFlatButton

class TodayProgress(Screen):
    def day_progress(self):
        mycursor = main.sqliteConnection.cursor()
        mycursor.execute("SELECT count(id_task) "
                         "FROM work_plan "
                         "WHERE scheduled_date = date('now') ")
        rows = mycursor.fetchone()
        count_of_types = str(rows[0])
        print(count_of_types)

        self.ids.today_stats.add_widget(
            MDRoundFlatButton(
                text=count_of_types + "\n\nT O - D O\nT A S K S",
                text_color=get_color_from_hex('#e5e5e5'),
                pos_hint={"x": .05, "y": .0},
                size_hint=(0.27, 0.35),
                font_size=15
            )
        )
        mycursor.execute("SELECT count(id_task) "
                         "FROM work_plan "
                         "WHERE done_date IS NOT NULL AND scheduled_date = date('now') ")
        rows = mycursor.fetchone()
        done_tasks_today = int(rows[0])
        mycursor.execute("SELECT count(id_task) "
                         "FROM work_plan "
                         "WHERE scheduled_date = date('now') ")
        rows = mycursor.fetchone()
        all_task_today = int(rows[0])
        if all_task_today == 0:
            precent = 0
        else:
            precent = int(done_tasks_today / all_task_today * 100)
        self.ids.today_stats.add_widget(
            MDRoundFlatButton(
                text=str(precent) + "%\n\nD O N E\nT A S K S",
                text_color=get_color_from_hex('#e5e5e5'),
                md_bg_color=get_color_from_hex('#333333'),
                pos_hint={"x": .365, "y": 0},
                size_hint=(0.27, 0.35),
                font_size=15
            )
        )

        mycursor.execute("SELECT count(id_task) "
                         "FROM work_plan "
                         "WHERE done_date IS NOT NULL AND scheduled_date = date('now') ")
        rows = mycursor.fetchone()
        done_tasks = int(rows[0])

        self.ids.today_stats.add_widget(
            MDRoundFlatButton(
                text=str(done_tasks) + "\n\nD O N E\nT A S K S",
                text_color=get_color_from_hex('#e5e5e5'),
                md_bg_color=get_color_from_hex('#333333'),
                pos_hint={"x": .68, "y": 0},
                size_hint=(0.27, 0.35),
                font_size=15

            )
        )
    def today_progress(self):
        self.ids.progress.add_widget(
            MDProgressBar(
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint_x=0.5,
                value=50,
                color=get_color_from_hex('#e5e5e5')

            )
        )

sm = ScreenManager()
sm.add_widget(TodayProgress(name="today_progress"))