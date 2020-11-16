import main
from kivy.uix.screenmanager import Screen, ScreenManager

class CreateTaskScreen(Screen):
    def add_task(self):

        name = self.ids.task_name.text
        time = self.ids.task_time.text

        mycursor = main.sqliteConnection.cursor()

        if name=="":
            print("Tu trzeba zrobić popup dla braku nazwy")
        elif time=="":
            print("Tu trzeba zrobić popup dla braku lub nieprawidłowego czasu")
        else:

            mycursor.execute(
                f" INSERT INTO task_type ( task_name, scheduled_time) \
                                                VALUES ('{self.ids.task_name.text}', '{self.ids.task_time.text}')")
            print("Done - number is bigger than 1")
            main.sqliteConnection.commit()


    def clear_inputs(self, text_inputs):
        for text_input in text_inputs:
            text_input.text = ""

sm = ScreenManager()
sm.add_widget(CreateTaskScreen(name="create_task_screen"))