import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanel
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.label import MDLabel
from functools import partial


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
                        on_press = partial(get_element_of_list, task_id[i],))
                )

        mycursor.execute(f"SELECT sum(a.scheduled_time) "
                         f"FROM task_type a "
                         f"JOIN work_plan b "
                         f"ON a.id_type=b.id_type "
                         f"WHERE b.scheduled_date = date('now')")
        row = mycursor.fetchone()
        try:
            time_on_this_date = int(row[0])
            print(time_on_this_date)

            self.ids.time.add_widget(
                MDLabel(
                    text = f"W O R K  T I M E: {str(time_on_this_date)} minutes",
                    halign= 'center',
                    pos_hint= {"center_x": 0.5, "center_y": 0.8},
                    theme_text_color= 'Custom',
                    text_color= get_color_from_hex('#3CB371'),
                    font_style= 'Caption',
                    font_size= 10
                )
            )
        except:
            self.ids.time.add_widget(
                MDLabel(
                    text="F R E E  T I M E! \nP L A N  Y O U R  D A Y",
                    halign='center',
                    pos_hint={"center_x": 0.5, "center_y": 0.8},
                    theme_text_color='Custom',
                    text_color=get_color_from_hex('#3CB371'),
                    font_style='Caption',
                    font_size=20
                )
            )
def get_element_of_list(the_element, zmienna_nadmiarowa):
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