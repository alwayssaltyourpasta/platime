import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from functools import partial
from kivy.properties import NumericProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.icon_definitions import md_icons


class ItemContent(MDBoxLayout):

    minutes = NumericProperty()

    def increment_time(self, interval):
        self.minutes += 1

    def start(self):
        Clock.unschedule(self.increment_time)
        Clock.schedule_interval(self.increment_time, 1)

    def stop(self):
        Clock.unschedule(self.increment_time)

    def end(self):
        self.dialog = MDDialog(
            text="Are you sure, you wanna save your time and end this task?",
            size_hint=[0.9, 0.5],
            auto_dismiss=False,
            buttons=[MDFlatButton(text="Yeah!", on_release=self.save_time),
                     MDFlatButton(text="Just reset the time", on_release=self.reset_time),
                     MDFlatButton(text="Not really", on_release=self.close_dialog)
                     ]
        )
        self.dialog.open()

    def reset_time(self, inst):
        self.minutes = 0
        self.dialog.dismiss()

    def delete_task(self):

        self.dialog = MDDialog(
            text="Are you sure, you wanna delete this task?",
            size_hint=[0.8, 0.5],
            auto_dismiss=False,
            buttons=[MDFlatButton(text="Yeah!", on_release=self.delete_from_db),
                     MDFlatButton(text="Not really", on_release=self.close_dialog)
                     ]
        )
        self.dialog.open()

    def done_task(self):

        self.dialog = MDDialog(
            text="Are you sure, have you done this task?",
            size_hint=[0.8, 0.5],
            auto_dismiss=False,
            buttons=[MDFlatButton(text="Yeah!", on_release=self.add_done_date),
                     MDFlatButton(text="Not really", on_release=self.close_dialog)
                     ]
        )
        self.dialog.open()

#back to today_screen without saving to database
    def close_dialog(self, inst):
        self.dialog.dismiss()

    #save to db, task done -> done date = no in today screen
    def save_time(self, inst):

        task_time = self.minutes
        task_id = task.zmienna

        mycursor = main.sqliteConnection.cursor()
        mycursor.execute(f"UPDATE work_plan SET execution_time = ?, done_date=date('now') WHERE id_task = ?", (task_time, task_id, ))
        main.sqliteConnection.commit()

        self.minutes = 0
        self.dialog.dismiss()

    #delete task from work plan
    def delete_from_db(self, inst):

        task_id_to_delete = int(task.zmienna)

        mycursor = main.sqliteConnection.cursor()
        mycursor.execute(f"DELETE FROM work_plan WHERE id_task=?",(task_id_to_delete,))
        main.sqliteConnection.commit()

        #TodayScreen().today()
        self.dialog.dismiss()

    #done date to task
    def add_done_date(self, init):

        done_task_id = int(task.zmienna)

        mycursor = main.sqliteConnection.cursor()
        mycursor.execute(f"UPDATE work_plan SET done_date = date('now') WHERE id_task = ?", (done_task_id,))
        main.sqliteConnection.commit()

        self.dialog.dismiss()


class TodayScreen(Screen):

    def today(self):

        mycursor = main.sqliteConnection.cursor()
        mycursor.execute("SELECT b.id_task, a.task_name, a.scheduled_time "
                         "FROM task_type a "
                         "JOIN work_plan b "
                         "ON a.id_type=b.id_type "
                         "WHERE b.scheduled_date = date('now') AND b.done_date IS NULL")
        rows = mycursor.fetchall()

        self.task_id = []
        self.task_name = []
        self.task_time = []

        for i in range(len(rows)):
            self.task_id.append(rows[i][0])
            self.task_name.append(rows[i][1])
            self.task_time.append(rows[i][2])

        for i in range(len(self.task_name)):
            self.ids.today_list.add_widget(
                MDExpansionPanel(
                    icon='graphics/bart.jpg',
                    content=ItemContent(),
                    panel_cls=MDExpansionPanelTwoLine(
                        text=f'{str(self.task_name[i])}',
                        secondary_text=f'{str(self.task_time[i])} minutes',
                        on_press = partial(task, self.task_id[i],)
                )))

        mycursor.execute(f"SELECT sum(a.scheduled_time) "
                         f"FROM task_type a "
                         f"JOIN work_plan b "
                         f"ON a.id_type=b.id_type "
                         f"WHERE b.scheduled_date = date('now') AND b.done_date IS NULL")
        row = mycursor.fetchone()

        try:
            time_on_this_date = int(row[0])

            self.ids.time.add_widget(
                MDLabel(
                    text = f"W O R K  T I M E: {str(time_on_this_date)} minutes",
                    halign= 'center',
                    pos_hint= {"center_x": 0.5, "center_y": 0.8},
                    theme_text_color= 'Custom',
                    text_color= get_color_from_hex('#3CB371'),
                    font_style= 'Caption',
                    font_size= 10
                )
            )

        except:

            self.ids.time.add_widget(
                MDLabel(
                    text="F R E E  T I M E! \nP L A N  Y O U R  D A Y",
                    halign='center',
                    pos_hint={"center_x": 0.5, "center_y": 0.8},
                    theme_text_color='Custom',
                    text_color=get_color_from_hex('#3CB371'),
                    font_style='Caption',
                    font_size=20
                )
            )

    
def task(name, nadmiar):
    task.zmienna = name


sm = ScreenManager()
sm.add_widget(TodayScreen(name="today_screen"))