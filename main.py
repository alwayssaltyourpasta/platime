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


#screens python files
import screens_py.today_screen
import screens_py.task_screen
import screens_py.statistics_screen
import screens_py.add_screen
import screens_py.create_task_screen
import screens_py.workplan_screen


#only for development
Window.size = (400,650)

#connection to db
try:
    sqliteConnection = sqlite3.connect('platime.db')
    print("Successfully Connected to SQLite")

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''
    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
        else:
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')
    icon = StringProperty("android")
class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass
class Content(MDBoxLayout):
    def show_datepicker(self):
        picker = MDDatePicker(callback=self.got_date)
        picker.open()

        # function which have to choose date add to tak in datebase
    def got_date(self, the_date):
        #print(the_date.year)
        #print(the_date.month)
        #print(the_date.day)
        type_t = 1
        print(the_date)
        save_to_db(type_t, the_date)

class MyContent(MDBoxLayout):
    def funkcja(self):
        print('hej')

def save_to_db(this_type, this_date):
    mycursor = sqliteConnection.cursor()
    mycursor.execute('SELECT a.id_type '
                     'FROM work_plan a '
                     'JOIN task_type b '
                     'ON a.id_type = b.id_type '
                     'WHERE b.task_name = ? ')
    mycursor.execute(f"INSERT INTO work_plan (id_type, scheduled_date) "
                     f"VALUES (?, ?)", (this_type, this_date))

    sqliteConnection.commit()
def work_plan(list):
    mycursor = sqliteConnection.cursor()

    mycursor.execute("SELECT id_type, task_name, scheduled_time FROM task_type")
    rows = mycursor.fetchall()

    task_id = []
    task_name = []
    task_time = []

    for i in range(len(rows)):
        task_id.append(rows[i][0])
        task_name.append(rows[i][1])
        task_time.append(rows[i][2])

    for i in range(len(task_name)):
        list.add_widget(
            ListItemWithCheckbox(text=f'{str(task_name[i])}',
                                 icon='circle-small',
                                 # secondary_text=f'Time: {str(task_time[i])} minutes',
                                 theme_text_color='Custom',
                                 text_color=get_color_from_hex('#e5e5e5'),
                                 font_style='Body1',
                                 # ten press umożliwi sprawdzenie ile czasu średnio potrzebne na zadanie wysunie się okno pod spodem
                                 on_press=lambda x: print(x.text))

        )
#funkcja na użytek kliknięcia elementu z listy
def click(name, zmienna_nadmiarowa):
    new = name
    print(new)
def show_tasks(task_list):
    mycursos = sqliteConnection.cursor()

    mycursos.execute("SELECT task_name, scheduled_time FROM task_type")
    rows = mycursos.fetchall()

    task_name = []
    task_time = []

    for i in range(len(rows)):
        task_name.append(rows[i][0])
        task_time.append(rows[i][1])
        #print(task_name[i])

    #print(rows)
    #print(task_name)
    for i in range(len(task_name)):
        task_list.add_widget(
            TwoLineListItem(text=f'Task: {str(task_name[i])}',
                            secondary_text=f'Time: {str(task_time[i])} minutes',
                            theme_text_color='Custom',
                            text_color=get_color_from_hex('#e5e5e5'),
                            font_style='Body1',
                            on_press=partial(click, task_name[i]))
        )


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
    def on_start(self):
        print('Start')

if __name__ == '__main__':
    PlatimeApp().run()