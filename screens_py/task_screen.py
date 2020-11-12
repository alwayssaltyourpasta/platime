import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
from kivy.utils import get_color_from_hex


class ListT(TwoLineAvatarIconListItem):
    def edit(self):
        print('I cyk zmiana')
    def delete(self):
        print('I cyk ni ma')


class ContainerT(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True

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
                    on_press=lambda x: print(x.text))
                )


sm = ScreenManager()
sm.add_widget(TaskScreen(name="task_screen"))