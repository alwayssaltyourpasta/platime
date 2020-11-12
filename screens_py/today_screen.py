import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanel
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch

today_element = ''


class TodayScreen(Screen):

    def today(self):
        mycursor = main.sqliteConnection.cursor()

        mycursor.execute("SELECT b.id_task, a.task_name, a.scheduled_time "
                         "FROM task_type a "
                         "JOIN work_plan b "
                         "ON a.id_type=b.id_type "
                         "WHERE b.scheduled_date = date('now') ")
        rows = mycursor.fetchall()

        task_id = []
        task_name = []
        task_time = []

        for i in range(len(rows)):
            task_id.append(rows[i][0])
            task_name.append(rows[i][1])
            task_time.append(rows[i][2])

        for i in range(len(task_name)):
            self.ids.today_list.add_widget(
                List(
                        text=f'{str(task_name[i])}',
                        secondary_text=f'{str(task_time[i])} minutes',
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#e5e5e5'),
                        font_style='Subtitle1',
                        on_press = lambda x: get_elemenf_of_list(x.text))
                )

def get_elemenf_of_list(the_element):
    today_element = the_element
    print(today_element)



class List(TwoLineAvatarIconListItem):
    def time(self):
        print('I cyk czas')
    def delete(self):
        print('I cyk ni ma')
    def done(self):
        print('I cyk zmiana')


class Container(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


sm = ScreenManager()
sm.add_widget(TodayScreen(name="today_screen"))