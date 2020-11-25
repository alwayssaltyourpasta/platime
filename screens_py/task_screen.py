import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
from kivy.utils import get_color_from_hex
from functools import partial
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.icon_definitions import md_icons

class ListT(TwoLineAvatarIconListItem):
    def delete(self):

        self.dialog = MDDialog(
            text="Are you sure, you wanna delete this task?",
            size_hint=[0.8, 0.5],
            auto_dismiss=False,
            buttons=[MDFlatButton(text="Yeah!", on_release=self.delete_from_db),
                     MDFlatButton(text="Not really", on_release=self.close_dialog)
                     ]
        )
        self.dialog.open()
#back to today_screen without saving to database
    def close_dialog(self, inst):
        self.dialog.dismiss()

#delete from db function
    def delete_from_db(self, inst):
        self.dialog.dismiss()

class TaskScreen(Screen):
    def all_tasks(self):
        mycursor = main.sqliteConnection.cursor()
        mycursor.execute("SELECT task_name, scheduled_time "
                         "FROM task_type ")
        rows = mycursor.fetchall()

        task_name = []
        task_time = []

        for i in range(len(rows)):
            task_name.append(rows[i][0])
            task_time.append(rows[i][1])

        for i in range(len(task_name)):
            self.ids.task_list.add_widget(
                ListT(
                    text=f'{str(task_name[i])}',
                    secondary_text=f'{str(task_time[i])} minutes',
                    theme_text_color='Custom',
                    text_color=get_color_from_hex('#e5e5e5'),
                    font_style='Subtitle1',
                    on_press=partial(task, task_name[i],))
                )
def task(name, nadmiar):
    task.zmienna = name
    print(task.zmienna)


sm = ScreenManager()
sm.add_widget(TaskScreen(name="task_screen"))