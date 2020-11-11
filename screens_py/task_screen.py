import main
from kivy.uix.screenmanager import Screen, ScreenManager


class TaskScreen(Screen):
    def all_tasks(self):
        main.work_plan(self.ids.task_list)

sm = ScreenManager()
sm.add_widget(TaskScreen(name="task_screen"))