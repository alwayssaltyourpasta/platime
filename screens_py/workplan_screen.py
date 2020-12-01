import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import TwoLineListItem
from kivy.utils import get_color_from_hex
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from functools import partial
from kivymd.uix.picker import MDDatePicker


class WorkPlanScreen(Screen):
    def show_datepicker(self):
        picker = MDDatePicker(callback=self.create_work_plan)
        picker.open()

    def create_work_plan(self, the_date):

        self.choose_date = str(the_date)
        mycursor = main.sqliteConnection.cursor()
        mycursor.execute(f"SELECT a.task_name, a.scheduled_time, b.id_task "
                         "FROM task_type a "
                         "JOIN work_plan b "
                         "ON a.id_type=b.id_type "
                         "WHERE b.scheduled_date = ? ", (self.choose_date,))
        rows = mycursor.fetchall()

        task_id = []
        task_name = []
        task_time = []

        for i in range(len(rows)):
            task_name.append(rows[i][0])
            task_time.append(rows[i][1])
            task_id.append(rows[i][2])

        for i in range(len(task_name)):
            self.ids.work_plan.add_widget(
                TwoLineListItem(
                    text=f'{str(task_name[i])}',
                    secondary_text=f'{str(task_time[i])} minutes',
                    theme_text_color='Custom',
                    text_color=get_color_from_hex('#e5e5e5'),
                    font_style='Subtitle1',
                    on_press=partial(self.create_dialog, task_id[i], )
                )
            )

        self.ids.date_label.add_widget(
            MDLabel(
                text=self.choose_date,
                halign='center',
                theme_text_color='Custom',
                text_color=get_color_from_hex('#3CB371'),
                font_style='Caption',
                font_size=8
            )
        )
        mycursor.execute(f"SELECT sum(a.scheduled_time) "
                         "FROM task_type a "
                         "JOIN work_plan b "
                         "ON a.id_type=b.id_type "
                         "WHERE b.scheduled_date = ? ", (self.choose_date,))
        row = mycursor.fetchone()
        try:
            all_time = int(row[0])

            self.ids.time_label.add_widget(
                MDLabel(
                    text=f"W O R K  T I M E: {str(all_time)} minutes",
                    halign='center',
                    theme_text_color='Custom',
                    text_color=get_color_from_hex('#3CB371'),
                    font_style='Caption',
                    font_size=8
                )
            )
        except:
            self.ids.time_label.add_widget(
                MDLabel(
                    text="F R E E  T I M E!",
                    halign='center',
                    theme_text_color='Custom',
                    text_color=get_color_from_hex('#3CB371'),
                    font_style='Caption',
                    font_size=8
                )
            )

    def create_dialog(self, task_id, nadmiar):

        self.task = int(task_id)
        self.dialog = MDDialog(
            text="What do you wanna do?",
            size_hint=[0.9, 0.5],
            auto_dismiss=False,
            buttons=[MDFlatButton(text="Back, please", on_release=self.close_dialog),
                     MDFlatButton(text="Delete this task", on_release=self.delete_from_db),
                     MDFlatButton(text="I've done yet", on_release=self.add_done_date)
            ]
        )
        self.dialog.open()

    def close_dialog(self, inst):
        self.dialog.dismiss()

    def delete_from_db(self, inst):
        print(self.task)
        mycursor = main.sqliteConnection.cursor()
        mycursor.execute(f"DELETE FROM work_plan WHERE id_task = ?", (self.task,))
        main.sqliteConnection.commit()

        self.ids.work_plan.clear_widgets()
        self.ids.time_label.clear_widgets()
        self.ids.date_label.clear_widgets()
        self.dialog.dismiss()
        self.show_datepicker()

    def add_done_date(self, init):
        print(self.task)
        mycursor = main.sqliteConnection.cursor()
        mycursor.execute(f"UPDATE work_plan SET done_date=date('now') WHERE id_task = ?", (self.task,))
        main.sqliteConnection.commit()

        self.ids.work_plan.clear_widgets()
        self.ids.time_label.clear_widgets()
        self.ids.date_label.clear_widgets()
        self.dialog.dismiss()
        self.show_datepicker()


sm = ScreenManager()
sm.add_widget(WorkPlanScreen(name="work_plan_screen"))