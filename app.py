from kivy.uix.screenmanager import Screen

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout


class AppBoxLayout(MDBoxLayout):
    pass

class StumpStickguyApp(MDApp):
    def build(self):
        #screen = Screen()
        #return screen
        return AppBoxLayout()


StumpStickguyApp().run()
