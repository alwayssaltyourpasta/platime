import main
from kivy.uix.screenmanager import Screen, ScreenManager

class WorkPlanScreen(Screen):
    def show_datepicker(self):

        picker = main.MDDatePicker(callback=self.got_date)
        picker.open()

        # function which have to choose date add to tak in datebase

    def got_date(self, the_date):
        main.work_plan(self.ids.work_plan)
        #tu zrobić wyświetlanie listy -> work plan z warunkiem ze scheduled-date rowna jest the date
        print(the_date.year)
        print(the_date.month)
        print(the_date.day)
        print(the_date)

sm = ScreenManager()
sm.add_widget(WorkPlanScreen(name="work_plan_screen"))