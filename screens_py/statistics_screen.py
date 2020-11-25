import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRoundFlatButton
from kivy.properties import NumericProperty, StringProperty
from kivy.utils import get_color_from_hex


class StatisticsScreen(Screen):

    def task(self):
        mycursor = main.sqliteConnection.cursor()
        mycursor.execute("SELECT count(id_type) FROM task_type")
        rows = mycursor.fetchone()
        count_of_types = str(rows[0])
        print(count_of_types)

        self.ids.buttons.add_widget(
            MDRoundFlatButton(
                text= count_of_types+"\n \nNumber of \nyour task types",
                text_color = get_color_from_hex('#e5e5e5'),
                pos_hint={"center_x": .5, "center_y": .5},
                size_hint=(0.25, 0.15),
                font_size = 20
            )
        )

        mycursor.execute("SELECT sum(execution_time) FROM work_plan")
        rows = mycursor.fetchone()
        execution_time = str(rows[0])
        print(execution_time)
        self.ids.buttons.add_widget(
            MDRoundFlatButton(
                text=execution_time,
                text_color=get_color_from_hex('#e5e5e5'),
                pos_hint={"center_x": .5, "center_y": .5},
                size_hint=(0.25, 0.15)
            )
        )
        mycursor.execute("SELECT sum(execution_time) FROM work_plan")
        rows = mycursor.fetchone()
        execution_time = str(rows[0])
        print(execution_time)
        self.ids.buttons.add_widget(
            MDRoundFlatButton(
                text=execution_time,
                text_color=get_color_from_hex('#e5e5e5'),
                pos_hint={"center_x": .5, "center_y": .5},
                size_hint=(0.25, 0.15)
            )
        )
        mycursor.execute("SELECT sum(execution_time) FROM work_plan")
        rows = mycursor.fetchone()
        execution_time = str(rows[0])
        print(execution_time)
        self.ids.buttons.add_widget(
            MDRoundFlatButton(
                text=execution_time,
                text_color=get_color_from_hex('#e5e5e5'),
                pos_hint={"center_x": .5, "center_y": .5},
                size_hint=(0.25, 0.15)
            )
        )
sm = ScreenManager()
sm.add_widget(StatisticsScreen(name="statistics_screen"))