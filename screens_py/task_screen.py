import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import TwoLineListItem
from kivy.utils import get_color_from_hex
from functools import partial
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class TaskScreen(Screen):
    def all_tasks(self):
        mycursor = main.sqliteConnection.cursor()
        mycursor.execute("SELECT id_type, task_name, scheduled_time "
                         "FROM task_type ")
        rows = mycursor.fetchall()
        task_id = []
        task_name = []
        task_time = []

        for i in range(len(rows)):
            task_id.append(rows[i][0])
            task_name.append(rows[i][1])
            task_time.append(rows[i][2])

        for i in range(len(task_name)):
            self.ids.task_list.add_widget(
                TwoLineListItem(
                    text=f'{str(task_name[i])}',
                    secondary_text=f'{str(task_time[i])} minutes',
                    theme_text_color='Custom',
                    text_color=get_color_from_hex('#e5e5e5'),
                    font_style='Subtitle1',
                    on_press=partial(self.delete_dialog, task_id[i],))
            )

    def delete_dialog(self, task_id, nadmiar):

        self.task = task_id
        self.dialog = MDDialog(
            text="Are you sure, you wanna delete this task?",
            size_hint=[0.8, 0.5],
            auto_dismiss=False,
            buttons=[MDFlatButton(text="Yeah!", on_release=self.delete_from_db),
                     MDFlatButton(text="Not really", on_release=self.close_dialog)
            ]
        )
        self.dialog.open()

    def close_dialog(self, inst):
        self.dialog.dismiss()

    def delete_from_db(self, inst):

        mycursor = main.sqliteConnection.cursor()
        mycursor.execute(f"DELETE FROM task_type WHERE id_type = ?", (self.task,))
        main.sqliteConnection.commit()

        self.ids.task_list.clear_widgets()
        self.all_tasks()
        self.dialog.dismiss()


sm = ScreenManager()
sm.add_widget(TaskScreen(name="task_screen"))