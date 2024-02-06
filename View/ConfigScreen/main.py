from kivymd.app import MDApp
from kivy.lang import Builder

class MyApp(MDApp):
    def build(self):
        return Builder.load_file('config_screen.kv')

if __name__ == '__main__':
    MyApp().run()