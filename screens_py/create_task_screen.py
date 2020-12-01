import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class CreateTaskScreen(Screen):
    def add_task(self):

        name = self.ids.task_name.text
        time = self.ids.task_time.text
        text1 = "Why don't you give anything?"
        text2 = "It's really important to give a name"
        text3 = "It's really important to give the time"
        text4 = "Please, back"
        text5 = "Ok, no problem"

        mycursor = main.sqliteConnection.cursor()

        if name=="" and time=="":
            self.dialog = MDDialog(
                text = text1,
                size_hint = [0.8, 0.5],
                auto_dismiss = False,
                buttons = [
                    MDFlatButton(
                        text = text4,
                        on_release=self.closeDialog)
                    ]
            )
            self.dialog.open()
        elif name=="":
            self.dialog = MDDialog(
                text = text2,
                size_hint = [0.8, 0.5],
                auto_dismiss = False,
                buttons = [
                    MDFlatButton(
                        text = text5,
                        on_release = self.closeDialog)
                ]
            )
            self.dialog.open()
        elif time=="":
            self.dialog = MDDialog(
                text = text3,
                size_hint = [0.8, 0.5],
                auto_dismiss = False,
                buttons = [
                    MDFlatButton(
                        text = text5,
                        on_release = self.closeDialog)
                ]
            )
            self.dialog.open()

        else:

            mycursor.execute(
                f"INSERT INTO task_type(task_name, scheduled_time) "
                f"VALUES ('{self.ids.task_name.text}', '{self.ids.task_time.text}')"
            )

            main.sqliteConnection.commit()

    def closeDialog(self, inst):
        self.dialog.dismiss()

    def clear_inputs(self, text_inputs):
        for text_input in text_inputs:
            text_input.text = ""

sm = ScreenManager()
sm.add_widget(CreateTaskScreen(name="create_task_screen"))