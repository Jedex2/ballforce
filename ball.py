from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock


class Ball(Widget):
    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 0, 0, 1)  # Set color (red in RGBA)
            self.ball = Ellipse(pos=self.center, size=(50, 50))  # Initial size and position

        self.velocity_y = 0  # Initial vertical velocity
        self.gravity = 1  # Gravity force

    def update(self, dt):
        # Apply gravity to the vertical velocity
        self.velocity_y -= self.gravity

        # Move the ball vertically
        self.ball.pos = (self.ball.pos[0], self.ball.pos[1] + self.velocity_y)

        # Bounce when the ball hits the bottom of the screen
        if self.ball.pos[1] < 0:
            self.ball.pos = (self.ball.pos[0], 0)
            self.velocity_y = -self.velocity_y * 0.8  # Bounce with some dampening

    def on_touch_down(self, touch):
        # Increase the vertical velocity when the screen is touched
        self.velocity_y += 20


class BallApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')

        self.ball = Ball()
        self.label = Label(text='Tap the screen to make the ball jump!', font_size='20sp')

        root.add_widget(self.label)
        root.add_widget(self.ball)

        # Schedule the update function to be called every 1/60 seconds (60 FPS)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

        return root

    def update(self, dt):
        # Update the ball's position
        self.ball.update(dt)


if __name__ == '__main__':
    BallApp().run()
