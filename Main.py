from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import MainScreen, HistoryScreen
from data_manager import DataManager

class MyApp(App):
    def build(self):
        self.data_manager = DataManager()
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(HistoryScreen(name='history'))
        return sm

if __name__ == '__main__':
    MyApp().run()
