import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.list import ThreeLineListItem


class TodayProgress(Screen):

    def day_progress(self):
        mycursor = main.sqliteConnection.cursor()
        mycursor.execute("SELECT count(id_task) "
                         "FROM work_plan "
                         "WHERE scheduled_date = date('now') AND done_date IS NULL ")
        rows = mycursor.fetchone()
        count_of_types = str(rows[0])

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
    def time(self):
        mycursor = main.sqliteConnection.cursor()
        mycursor.execute("select a.task_name, a.scheduled_time, b.execution_time, avg(b.execution_time) "
                         "from task_type a "
                         "join work_plan b "
                         "on a.id_type = b.id_type "
                         "where b.scheduled_date = date('now') "
                         "group by b.id_type ")
        rows = mycursor.fetchall()

        task_name = []
        task_time = []
        real_time = []
        avg_time = []

        for i in range(len(rows)):
            task_name.append(rows[i][0])
            task_time.append(rows[i][1])
            real_time.append(rows[i][2])
            avg_time.append(rows[i][3])
        print(avg_time)
        for i in range(len(task_name)):
            if real_time[i]==None:
                precent = "You need to measure the time first"
            else:
                precent = str(int(real_time[i]/task_time[i]*100))+"%"
            if avg_time[i]==None:
                avg_time[i]=str(avg_time[i])
            else:
                avg_time[i]=int(avg_time[i])
            self.ids.progress.add_widget(
                ThreeLineListItem(
                    text = str(task_name[i]),
                    secondary_text= str(real_time[i])+"/"+str(task_time[i])+"/"+str(avg_time[i]),
                    tertiary_text = precent
                )
            )
    def summary(self):
        mycursor = main.sqliteConnection.cursor()

        mycursor.execute("SELECT sum(execution_time) "
                         "FROM work_plan "
                         "WHERE done_date = date('now')")
        rows = mycursor.fetchone()
        time = rows[0]

        mycursor.execute("SELECT a.task_name, max(b.execution_time) "
                         "FROM task_type a "
                         "JOIN work_plan b "
                         "ON a.id_type=b.id_type "
                         "WHERE done_date = date('now') ")
        row = mycursor.fetchone()
        max_task = row[0]
        max_time = row[1]

        mycursor.execute("SELECT a.task_name, min(b.execution_time) "
                         "FROM task_type a "
                         "JOIN work_plan b "
                         "ON a.id_type=b.id_type "
                         "WHERE done_date = date('now') ")
        row = mycursor.fetchone()
        min_task = row[0]
        min_time = row[1]

        self.ids.analysis.add_widget(
            MDRoundFlatButton(
                text="TOTAL TIME UTILIZED: "+str(time),
                text_color=get_color_from_hex('#e5e5e5'),
                pos_hint={"x": 0, "y": 0.30},
                size_hint=(1, 0.1),
                font_size=13
            )
        )
        self.ids.analysis.add_widget(
            MDRoundFlatButton(
                text="MOST TIME SPENT ON: "+str(max_task) +" - "+ str(max_time),
                text_color=get_color_from_hex('#e5e5e5'),
                pos_hint={"x": 0, "y": 0.15},
                size_hint=(1, 0.1),
                font_size=13
            )
        )
        self.ids.analysis.add_widget(
            MDRoundFlatButton(
                text="LEAST TIME SPENT ON: "+str(min_task) +" - "+ str(min_time),
                text_color=get_color_from_hex('#e5e5e5'),
                pos_hint={"x": 0, "y": 0},
                size_hint=(1, 0.1),
                font_size=13
            )
        )


sm = ScreenManager()
sm.add_widget(TodayProgress(name="today_progress"))