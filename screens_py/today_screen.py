import main
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanel
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.label import MDLabel
from functools import partial
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivy.properties import NumericProperty

today_element = ''

class ItemContent(MDBoxLayout):
    seconds = NumericProperty()
    minutes = NumericProperty()

    def increment_time(self, interval):
        self.minutes += 1

    def start(self):
        Clock.unschedule(self.increment_time)
        Clock.schedule_interval(self.increment_time, 1)




    def stop(self):
        Clock.unschedule(self.increment_time)

    def end(self):
        #popup - czy zerować czy zapisać czas i zadanie zrobione
        print('popup tu ma byc')

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
                MDExpansionPanel(
                    icon='logo.png',
                    content=ItemContent(),
                    panel_cls=MDExpansionPanelTwoLine(
                        text=f'{str(task_name[i])}',
                        secondary_text=f'{str(task_time[i])} minutes')

                ))



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

        def on_panel_open(self, instance_panel):
            print(instance_panel)

def get_id(task, nadmiarowa):
    id_task = task
    print(id_task)




sm = ScreenManager()
sm.add_widget(TodayScreen(name="today_screen"))