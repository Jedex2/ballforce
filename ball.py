from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class BallApp(App):
    def build(self):
        return GridLayout()

if __name__ == '__main__':
    BallApp().run()