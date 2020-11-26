import main
from kivy.uix.screenmanager import Screen, ScreenManager
import datetime
from datetime import datetime, timedelta
from kivymd.uix.button import MDRoundFlatButton
from kivy.utils import get_color_from_hex
from kivymd.uix.list import ThreeLineListItem


class MonthProgress(Screen):
    def month_summary(self):
        dt = datetime.today()
        month = dt.date()-timedelta(days=30)
        print(month)

        mycursor = main.sqliteConnection.cursor()
        mycursor.execute(f"SELECT count(id_task) "
                         f"FROM work_plan "
                         f"WHERE done_date > ? AND done_date <= date('now') ", (month,))
        row = mycursor.fetchone()
        done_tasks_during_month = row[0]
        print(done_tasks_during_month)

        self.ids.month_stats.add_widget(
            MDRoundFlatButton(
                text=str(done_tasks_during_month) + "\n\nD O N E\nT A S K S",
                text_color=get_color_from_hex('#e5e5e5'),
                pos_hint={"x": .05, "y": .0},
                size_hint=(0.27, 0.35),
                font_size=15
            )
        )
        mycursor.execute(f"SELECT count(id_task) "
                         f"FROM work_plan "
                         f"WHERE scheduled_date > ? AND scheduled_date <= date('now') ", (month,))
        row = mycursor.fetchone()
        all_scheduled_tasks = row[0]
        if all_scheduled_tasks == None:
            precent = 'PRO8LEM'
        else:
            precent = int(done_tasks_during_month/all_scheduled_tasks*100)
        print(precent)
        self.ids.month_stats.add_widget(
            MDRoundFlatButton(
                text=str(precent) + "%\n\nD O N E\nT A S K S",
                text_color=get_color_from_hex('#e5e5e5'),
                md_bg_color=get_color_from_hex('#333333'),
                pos_hint={"x": .365, "y": 0},
                size_hint=(0.27, 0.35),
                font_size=15
            )
        )
        mycursor.execute("SELECT sum(execution_time) "
                         "FROM work_plan "
                         "WHERE done_date <= date('now') AND done_date > ? ", (month,))
        rows = mycursor.fetchone()
        month_time = rows[0]
        self.ids.month_stats.add_widget(
            MDRoundFlatButton(
                text=str(month_time) + "\nminutes\n\nW O R K\nT I M E",
                text_color=get_color_from_hex('#e5e5e5'),
                pos_hint={"x": .68, "y": 0},
                size_hint=(0.27, 0.35),
                font_size=15
            )
        )

    def month_analysis(self):
        dt = datetime.today()
        month = dt.date() - timedelta(days=30)
        print(month)
        mycursor = main.sqliteConnection.cursor()
        mycursor.execute(f"select a.task_name, a.scheduled_time, avg(b.execution_time), count(b.id_task), count(b.done_date) "
                         f"from task_type a "
                         f"join work_plan b "
                         f"on a.id_type = b.id_type "
                         f"where b.scheduled_date <= date('now') AND scheduled_date > ?"
                         f"group by b.id_type ", (month,))
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
        print(number_of_task)
        print(done_tasks)
        for i in range(len(task_name)):

            if avg_time[i]==None:
                time_precent = "None"

            else:
                time_precent = str(int(avg_time[i]/task_time[i]*100))+"%"

            if done_tasks[i]==None:
                task_precent = "None"
            else:
                time_precent = str(int(done_tasks[i]/number_of_task[i]*100)) + "%"

            if avg_time[i] == None:
                avg_time[i] = str(avg_time[i])
            else:
                avg_time[i] = int(avg_time[i])


            self.ids.month_progress.add_widget(
                ThreeLineListItem(
                    text=str(task_name[i]),
                    secondary_text=str(done_tasks[i])+"/"+str(number_of_task[i])+"/"+time_precent,
                    tertiary_text=str(task_time[i]) + "/" + str(avg_time[i]) +"/"+ time_precent
                )
            )

sm = ScreenManager()
sm.add_widget(MonthProgress(name="month_progress"))