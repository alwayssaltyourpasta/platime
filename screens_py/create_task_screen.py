import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class CreateTaskScreen(Screen):
    def add_task(self):

        name = self.ids.task_name.text
        time = self.ids.task_time.text

        mycursor = main.sqliteConnection.cursor()
        mycursor.execute("SELECT id_type FROM task_type ")
        rows = mycursor.fetchall()

        if name=="" and time=="":
            self.dialog = MDDialog(
                text="Why don't you give anything?",
                size_hint=[0.8, 0.5],
                auto_dismiss=False,
                buttons=[MDFlatButton(text="Please, back", on_release=self.closeDialog)
                         ]
            )
            self.dialog.open()
        elif name=="":
            self.dialog = MDDialog(
                text = "It's really important to give a name to your task",
                size_hint=[0.8, 0.5],
                auto_dismiss = False,
                buttons = [
                    MDFlatButton(text = "OK, no problem", on_release = self.closeDialog)
                ]
            )
            self.dialog.open()
        elif time=="":
            self.dialog = MDDialog(
                text="It's really important to give the time for the task",
                size_hint=[0.8, 0.5],
                auto_dismiss=False,
                buttons=[MDFlatButton(text = "OK, no problem", on_release = self.closeDialog)
                ]
            )
            self.dialog.open()

        else:

            mycursor.execute(
                f" INSERT INTO task_type ( task_name, scheduled_time) \
                                                VALUES ('{self.ids.task_name.text}', '{self.ids.task_time.text}')")
            print("Done")
            main.sqliteConnection.commit()

    #close dialog with warnings
    def closeDialog(self, inst):
        self.dialog.dismiss()

    def clear_inputs(self, text_inputs):
        for text_input in text_inputs:
            text_input.text = ""

sm = ScreenManager()
sm.add_widget(CreateTaskScreen(name="create_task_screen"))