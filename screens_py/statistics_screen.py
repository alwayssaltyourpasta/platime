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
                text= count_of_types+"\n\n\nT A S K \nT Y P E S",
                text_color = get_color_from_hex('#e5e5e5'),
                pos_hint={"x": .05, "y": .6},
                size_hint=(0.4, 0.35),
                font_size = 20
            )
        )

        mycursor.execute("SELECT sum(execution_time) FROM work_plan")
        rows = mycursor.fetchone()
        execution_time = str(rows[0])
        print(execution_time)
        self.ids.buttons.add_widget(
            MDRoundFlatButton(
                text=execution_time+"\nminutes \n\nW O R K\nT I M E",
                text_color=get_color_from_hex('#e5e5e5'),
                pos_hint={"x": .55, "y": .6},
                size_hint=(0.4, 0.35),
                font_size=20
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
                pos_hint={"x": .05, "y": .2},
                size_hint=(0.4, 0.35)
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
                pos_hint={"x": .55, "y": .2},
                size_hint=(0.4, 0.35)
            )
        )
sm = ScreenManager()
sm.add_widget(StatisticsScreen(name="statistics_screen"))