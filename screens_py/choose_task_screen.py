import main
from kivy.uix.screenmanager import Screen, ScreenManager

class ChooseTaskScreen(Screen):

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
                main.ListItemWithCheckbox(text=f'{str(task_name[i])}',
                                          icon = 'circle-small',
                                          theme_text_color='Custom',
                                          text_color=main.get_color_from_hex('#e5e5e5'),
                                          font_style='Body1',
                                          #ten press umożliwi sprawdzenie ile czasu średnio potrzebne na zadanie wysunie się okno pod spodem
                                          on_press=lambda x: print(x.text)
                                          )
                )

sm = ScreenManager()
sm.add_widget(ChooseTaskScreen(name="choose_task_screen"))