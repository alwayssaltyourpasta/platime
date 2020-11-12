import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
from kivy.utils import get_color_from_hex
from kivymd.uix.label import MDLabel


class ListW(TwoLineAvatarIconListItem):
    def edit(self):
        print('I cyk zmiana')
    def delete(self):
        print('I cyk ni ma')


class ContainerW(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class WorkPlanScreen(Screen):
    def show_datepicker(self):

        picker = main.MDDatePicker(callback=self.got_date)
        picker.open()

        # function which have to choose date add to tak in datebase

    def got_date(self, the_date):
        print(the_date)
        work_plan_f(self, the_date)

        #tu zrobić wyświetlanie listy -> work plan z warunkiem ze scheduled-date rowna jest the date

def work_plan_f(self, date_new):
    string_date = str(date_new)
    print(string_date)
    mycursor = main.sqliteConnection.cursor()
    mycursor.execute(f"SELECT a.task_name, a.scheduled_time "
                     "FROM task_type a "
                     "JOIN work_plan b "
                     "ON a.id_type=b.id_type "
                     "WHERE b.scheduled_date = ? ", (string_date,))
    rows = mycursor.fetchall()


    task_name = []
    task_time = []

    for i in range(len(rows)):

        task_name.append(rows[i][0])
        task_time.append(rows[i][1])

    self.ids.ciekawe.add_widget(
        MDLabel(
            text=string_date,
            halign='center',
            theme_text_color= 'Custom',
            text_color= get_color_from_hex('#3CB371'),
            font_style= 'Caption',
            font_size= 8
    )
    )

    for i in range(len(task_name)):
        self.ids.work_plan.add_widget(
            ListW(
                text=f'{str(task_name[i])}',
                secondary_text=f'{str(task_time[i])} minutes',
                theme_text_color='Custom',
                text_color=get_color_from_hex('#e5e5e5'),
                font_style='Subtitle1')
        )
sm = ScreenManager()
sm.add_widget(WorkPlanScreen(name="work_plan_screen"))