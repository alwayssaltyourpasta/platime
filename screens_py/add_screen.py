import main
from kivy.uix.screenmanager import Screen, ScreenManager

class AddScreen(Screen):
    date_db = ''
    def add_to_db(self, date_to_db):
        task_l = self.ids.choose_list
        main.show_tasks(task_l)

    def show_datepicker(self):
        picker = main.MDDatePicker(callback=self.got_date)
        picker.open()

        # function which have to choose date add to tak in datebase

    def got_date(self, the_date):
        task_date = the_date
        print(the_date.year)
        print(the_date.month)
        print(the_date.day)
        print(the_date)
        type_tt = 7
        main.save_to_db(type_tt, task_date)

sm = ScreenManager()
sm.add_widget(AddScreen(name="add_screen"))