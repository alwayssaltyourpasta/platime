import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import TwoLineAvatarIconListItem
from functools import partial


class TaskList(TwoLineAvatarIconListItem):
    pass


class AddTaskScreen(Screen):

    def choose_task(self):
        mycursor = main.sqliteConnection.cursor()

        mycursor.execute("SELECT id_type, task_name, scheduled_time FROM task_type")
        rows = mycursor.fetchall()

        task_id = []
        task_name = []
        task_time = []

        for i in range(len(rows)):
            task_id.append(rows[i][0])
            task_name.append(rows[i][1])
            task_time.append(rows[i][2])

        for i in range(len(task_name)):
            self.ids.choose_list.add_widget(
                TaskList(
                    text=f'{str(task_name[i])}',
                    secondary_text=f'{str(task_time[i])} minutes',
                    theme_text_color='Custom',
                    text_color=main.get_color_from_hex('#e5e5e5'),
                    font_style='Body1',
                    on_press=partial(self.choosen_task, task_id[i],)
                )
            )

    def choosen_task(self, task_from_list, nadmiarowa_zmienna):
        self.task_n = int(task_from_list)
        picker = main.MDDatePicker(callback=self.save_to_database)
        picker.open()

    def save_to_database(self, the_date):
        task_date = str(the_date)
        task_id = self.task_n

        mycursor = main.sqliteConnection.cursor()
        mycursor.execute(f"INSERT INTO work_plan (id_type, scheduled_date) "
                         f"VALUES (?,?)", (task_id, task_date))

        main.sqliteConnection.commit()


sm = ScreenManager()
sm.add_widget(AddTaskScreen(name="add_task_screen"))