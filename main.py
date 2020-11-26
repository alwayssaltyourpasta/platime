from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from design import builder_string
from kivy.core.window import Window
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.list import TwoLineListItem
from kivy.utils import get_color_from_hex
from functools import partial
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
import sqlite3
from kivy.uix.checkbox import CheckBox
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import NumericProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivy.clock import Clock


#screens python files
import screens_py.today_screen
import screens_py.task_screen
import screens_py.statistics_screen
import screens_py.add_screen
import screens_py.create_task_screen
import screens_py.workplan_screen
import screens_py.today_progress_screen
import screens_py.month_progress_screen
import screens_py.year_progress_screen


#only for development
Window.size = (400,650)

#connection to db
try:
    sqliteConnection = sqlite3.connect('platime.db')
    print("Successfully Connected to SQLite")

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

class Start(Screen):
    def skip(self, dt):
        self.manager.current = "today_screen"

    def on_enter(self, *args):
        Clock.schedule_once(self.skip, 0)


#main class - app
class PlatimeApp(MDApp):
    def __init__(self, **kwargs):
        super(PlatimeApp, self).__init__(**kwargs)

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "300"
        self.theme_cls.theme_style = "Dark"
        self.icon = 'plik.png'
        screen = Screen()
        self.read_design = Builder.load_string(builder_string)
        screen.add_widget(self.read_design)
        return screen


if __name__ == '__main__':
    PlatimeApp().run()