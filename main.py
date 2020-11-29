from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from design import builder_string
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import sqlite3
from kivy.clock import Clock
import datetime
from datetime import datetime, timedelta
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.picker import MDDatePicker


#screens python files
import screens_py.today_screen
import screens_py.task_screen
import screens_py.statistics_screen
import screens_py.add_screen
import screens_py.create_task_screen
import screens_py.workplan_screen
import screens_py.today_progress_screen
import screens_py.month_progress_screen
import screens_py.year_progress_screen


#only for development
Window.size = (400,650)

#connection to db
try:
    sqliteConnection = sqlite3.connect('platime.db')
    print("Successfully Connected to SQLite")

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

class Start(Screen):
    def skip(self, dt):
        self.manager.current = "today_screen"

    def on_enter(self, *args):
        Clock.schedule_once(self.skip, 0)

#analysis function
def summary(self, number_of_days, main_list):
    dt = datetime.today()
    days = dt.date()-timedelta(days=number_of_days)


    mycursor = sqliteConnection.cursor()
    mycursor.execute(f"SELECT count(id_task) "
                        f"FROM work_plan "
                        f"WHERE done_date > ? AND done_date <= date('now') ", (days,))
    row = mycursor.fetchone()
    done_tasks = row[0]


    main_list.add_widget(
        MDRoundFlatButton(
            text=str(done_tasks) + "\n\nD O N E\nT A S K S",
            text_color=get_color_from_hex('#e5e5e5'),
            pos_hint={"x": .05, "y": .0},
            size_hint=(0.27, 0.35),
            font_size=15
            )
        )
    mycursor.execute(f"SELECT count(id_task) "
                         f"FROM work_plan "
                         f"WHERE scheduled_date > ? AND scheduled_date <= date('now') ", (days,))
    row = mycursor.fetchone()
    all_scheduled_tasks = row[0]

    if all_scheduled_tasks == 0:
        precent = '0'
    else:
        precent = int(done_tasks/all_scheduled_tasks*100)

    main_list.add_widget(
        MDRoundFlatButton(
            text=str(precent) + "%\n\nD O N E\nT A S K S",
            text_color=get_color_from_hex('#e5e5e5'),
            md_bg_color=get_color_from_hex('#333333'),
            pos_hint={"x": .365, "y": 0},
            size_hint=(0.27, 0.35),
            font_size=15
            )
        )
    mycursor.execute("SELECT SUM(execution_time) "
                        "FROM work_plan "
                        "WHERE done_date <= DATE('now') AND done_date > ? ", (days,))
    rows = mycursor.fetchone()
    time = rows[0]
    if time == None:
        time = "0"
    else:
        time = time
    main_list.add_widget(
        MDRoundFlatButton(
            text=str(time) + "\nminutes\n\nW O R K\nT I M E",
            text_color=get_color_from_hex('#e5e5e5'),
            pos_hint={"x": .68, "y": 0},
            size_hint=(0.27, 0.35),
            font_size=15
            )
        )

def analysis(self, number_of_days, scroll_list):
    dt = datetime.today()
    days = dt.date() - timedelta(days=number_of_days)
    print(days)
    mycursor = sqliteConnection.cursor()
    mycursor.execute(
        f"SELECT a.task_name, a.scheduled_time, AVG(b.execution_time), COUNT(b.id_task), count(b.done_date) "
        f"FROM task_type a "
        f"JOIN work_plan b "
        f"ON a.id_type = b.id_type "
        f"WHERE b.scheduled_date <= DATE('now') AND scheduled_date > ?"
        f"GROUP BY b.id_type ", (days,))
    rows = mycursor.fetchall()

    task_name = []
    task_time = []
    avg_time = []
    number_of_task = []
    done_tasks = []

    for i in range(len(rows)):
        task_name.append(rows[i][0])
        task_time.append(rows[i][1])
        avg_time.append(rows[i][2])
        number_of_task.append(rows[i][3])
        done_tasks.append(rows[i][4])

    for i in range(len(task_name)):

        if avg_time[i] == None:
            time_precent = "0"

        else:
            time_precent = str(int(avg_time[i] / task_time[i] * 100)) + "%"

        if done_tasks[i] == None:
            task_precent = "0"
        else:
            task_precent = str(int(done_tasks[i] / number_of_task[i] * 100)) + "%"

        if avg_time[i] == None:
            avg_time[i] = str(avg_time[i])
        else:
            avg_time[i] = int(avg_time[i])

        scroll_list.add_widget(
            ThreeLineListItem(
                text=str(task_name[i]),
                secondary_text=str(done_tasks[i]) + "/" + str(number_of_task[i]) + "/" + task_precent,
                tertiary_text=str(task_time[i]) + "/" + str(avg_time[i]) + "/" + time_precent
            )
        )


#main class - app
class PlatimeApp(MDApp):
    def __init__(self, **kwargs):
        super(PlatimeApp, self).__init__(**kwargs)

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "300"
        self.theme_cls.theme_style = "Dark"
        self.icon = 'plik.png'
        screen = Screen()
        self.read_design = Builder.load_string(builder_string)
        screen.add_widget(self.read_design)
        return screen



if __name__ == '__main__':
    PlatimeApp().run()