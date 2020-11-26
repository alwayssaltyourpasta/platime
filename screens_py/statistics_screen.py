import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRoundFlatButton
from kivy.utils import get_color_from_hex
from kivymd.uix.progressbar import MDProgressBar
from functools import partial
from kivymd.uix.label import MDLabel


class StatisticsScreen(Screen):

    def task(self):

        mycursor = main.sqliteConnection.cursor()
        mycursor.execute("SELECT count(id_type) "
                         "FROM task_type ")
        rows = mycursor.fetchone()
        count_of_types = str(rows[0])
        print(count_of_types)

        self.ids.buttons.add_widget(
            MDRoundFlatButton(
                text= count_of_types+"\n\nT A S K \nT Y P E S",
                text_color = get_color_from_hex('#e5e5e5'),
                pos_hint={"x": .05, "y": .6},
                size_hint=(0.4, 0.35),
                font_size = 15

            )
        )
        mycursor.execute("SELECT count(id_task) "
                         "FROM work_plan "
                         "WHERE done_date IS NOT NULL ")
        rows = mycursor.fetchone()
        execution_time = int(rows[0])
        mycursor.execute("SELECT count(id_task) "
                         "FROM work_plan ")
        rows = mycursor.fetchone()
        all_time = int(rows[0])
        if all_time == 0:
            precent = 0
        else:
            precent = int(execution_time / all_time * 100)
        self.ids.buttons.add_widget(
            MDRoundFlatButton(
                text=str(execution_time) + "\n\nD O N E\nT A S K S",
                text_color=get_color_from_hex('#e5e5e5'),
                md_bg_color=get_color_from_hex('#333333'),
                pos_hint={"x": .55, "y": .6},
                size_hint=(0.4, 0.35),
                font_size=15
            )
        )

        mycursor.execute("SELECT count(id_task) "
                         "FROM work_plan "
                         "WHERE done_date IS NOT NULL  ")
        rows = mycursor.fetchone()
        done_tasks = int(rows[0])
        mycursor.execute("SELECT count(id_task) "
                         "FROM work_plan ")
        rows = mycursor.fetchone()
        to_do_tasks = int(rows[0])
        if to_do_tasks==0:
            workplan = 0
        else:
            workplan = int(done_tasks/to_do_tasks*100)
        self.ids.buttons.add_widget(
            MDRoundFlatButton(
                text=str(workplan)+"%\n\nD O N E\nW O R K\nP L A N",
                text_color=get_color_from_hex('#e5e5e5'),
                md_bg_color=get_color_from_hex('#333333'),
                pos_hint={"x": .05, "y": .2},
                size_hint=(0.4, 0.35),
                font_size=15

            )
        )
        mycursor.execute("SELECT sum(execution_time) "
                         "FROM work_plan ")
        rows = mycursor.fetchone()
        execution_time = str(rows[0])
        print(execution_time)
        self.ids.buttons.add_widget(
            MDRoundFlatButton(
                text=execution_time + "\nminutes \n\nW O R K\nT I M E",
                text_color=get_color_from_hex('#e5e5e5'),
                md_bg_color=get_color_from_hex('#333333'),
                pos_hint={"x": .55, "y": .2},
                size_hint=(0.4, 0.35),
                font_size=15
            )
        )



sm = ScreenManager()
sm.add_widget(StatisticsScreen(name="statistics_screen"))


