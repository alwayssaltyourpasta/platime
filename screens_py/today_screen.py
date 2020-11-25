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
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class ItemContent(MDBoxLayout):


    minutes = NumericProperty()

    def increment_time(self, interval):
        self.minutes += 1

    def start(self):
        Clock.unschedule(self.increment_time)
        Clock.schedule_interval(self.increment_time, 60)

    def stop(self):
        Clock.unschedule(self.increment_time)

    def end(self):
        self.dialog = MDDialog(
            text="Are you sure, you wanna save your time and end this task?",
            size_hint=[0.8, 0.5],
            auto_dismiss=False,
            buttons=[MDFlatButton(text="Yeah!", on_release=self.save_time),
                     MDFlatButton(text="Not really", on_release=self.close_dialog)
                     ]
        )
        self.dialog.open()
    def delete_task(self):
        self.dialog = MDDialog(
            text="Are you sure, you wanna delete this task?",
            size_hint=[0.8, 0.5],
            auto_dismiss=False,
            buttons=[MDFlatButton(text="Yeah!", on_release=self.delete_from_db),
                     MDFlatButton(text="Not really", on_release=self.close_dialog)
                     ]
        )
        self.dialog.open()
    def done_task(self):
        self.dialog = MDDialog(
            text="Are you sure, have you done this task?",
            size_hint=[0.8, 0.5],
            auto_dismiss=False,
            buttons=[MDFlatButton(text="Yeah!", on_release=self.add_done_date),
                     MDFlatButton(text="Not really", on_release=self.close_dialog)
                     ]
        )
        self.dialog.open()
#back to today_screen without saving to database
    def close_dialog(self, inst):
        self.dialog.dismiss()
#save to db, task done -> done date = no in today screen
    def save_time(self, inst):
        self.dialog.dismiss()
#delete from db function
    def delete_from_db(self, inst):
        self.dialog.dismiss()
#add done date to id task that makes task done and not show it on main screen
    def add_done_date(self, init):
        self.dialog.dismiss()
class TodayScreen(Screen):

    def today(self):

        mycursor = main.sqliteConnection.cursor()

        mycursor.execute("SELECT b.id_task, a.task_name, a.scheduled_time "
                         "FROM task_type a "
                         "JOIN work_plan b "
                         "ON a.id_type=b.id_type "
                         "WHERE b.scheduled_date = date('now') ")
        rows = mycursor.fetchall()

        self.task_id = []
        self.task_name = []
        self.task_time = []

        for i in range(len(rows)):
            self.task_id.append(rows[i][0])
            self.task_name.append(rows[i][1])
            self.task_time.append(rows[i][2])

        for i in range(len(self.task_name)):
            self.ids.today_list.add_widget(
                Panel(
                    icon='logo.png',
                    content=ItemContent(),
                    panel_cls=MDExpansionPanelTwoLine(
                        text=f'{str(self.task_name[i])}',
                        secondary_text=f'{str(self.task_time[i])} minutes')

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

class Panel(MDExpansionPanel):
    def on_open(self, *args):
        pobranie_z_today = 'hmmmmm'
        print(pobranie_z_today)

sm = ScreenManager()
sm.add_widget(TodayScreen(name="today_screen"))