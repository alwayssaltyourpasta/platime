import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import TwoLineListItem, TwoLineAvatarIconListItem
from functools import partial


class TaskList(TwoLineAvatarIconListItem):
    pass
class AddTaskScreen(Screen):

    def choose_task(self):
        mycursor = main.sqliteConnection.cursor()

        mycursor.execute("SELECT task_name, scheduled_time FROM task_type")
        rows = mycursor.fetchall()

        task_name = []
        task_time = []

        for i in range(len(rows)):
            task_name.append(rows[i][0])
            task_time.append(rows[i][1])

        for i in range(len(task_name)):
            self.ids.choose_list.add_widget(
                TaskList(
                    text=f'{str(task_name[i])}',
                    secondary_text=f'{str(task_time[i])} minutes',
                    theme_text_color='Custom',
                    text_color=main.get_color_from_hex('#e5e5e5'),
                    font_style='Body1',
                    #ten press umożliwi sprawdzenie ile czasu średnio potrzebne na zadanie wysunie się okno pod spodem
                    on_press=partial(self.choosen_task, task_name[i],)
                    )
                )
    #this function call calendar
    def choosen_task(self, task_from_list, nadmiarowa_zmienna):
        self.task_n = task_from_list
        picker = main.MDDatePicker(callback=self.save_to_database)
        picker.open()

    #this function is database saver
    def save_to_database(self, the_date):
        task_date = the_date
        task_name = self.task_n

        print(task_name)
        print(task_date)

        mycursor = main.sqliteConnection.cursor()
        mycursor.execute('SELECT id_type '
                         'FROM task_type '
                         'WHERE task_name = ? ', (task_name,))

        row = mycursor.fetchone()
        print(row)
        this_type = int(row[0])
        print(this_type)

        mycursor.execute(f"INSERT INTO work_plan (id_type, scheduled_date) "
                         f"VALUES (?, ?)", (this_type, task_date))

        main.sqliteConnection.commit()



sm = ScreenManager()
sm.add_widget(AddTaskScreen(name="add_task_screen"))