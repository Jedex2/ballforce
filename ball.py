from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Ellipse, Color, Rectangle
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import random

class Ball(Widget):
    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        with self.canvas:
            # Draw the background rectangle
            Color(0, 0, 0, 1)  # Set color (black in RGBA) for the background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

            # Draw the ball
            self.ball_color = Color(1, 0, 0, 1)  # Set color (red in RGBA) for the ball
            self.ball = Ellipse(pos=(self.center_x - 25, self.center_y - 25), size=(50, 50))
            self.canvas.add(self.ball_color)

        self.velocity_x = 0  # Initial horizontal velocity
        self.velocity_y = 0  # Initial vertical velocity
        self.gravity = 1  # Gravity force
        self.damping = 0.9  # Damping factor for reducing velocity on each bounce
        self.bounce_count = 0  # Initialize bounce count

    def update(self, dt):
        # Apply gravity to the vertical velocity
        self.velocity_y -= self.gravity

        # Move the ball horizontally and vertically
        self.ball.pos = (self.ball.pos[0] + self.velocity_x, self.ball.pos[1] + self.velocity_y)

        # Bounce off the bottom edge
        if self.ball.pos[1] < 0:
            self.ball.pos = (self.ball.pos[0], 0)
            self.velocity_y = -self.velocity_y * self.damping  # Bounce with damping

        # Bounce off the top edge
        if self.ball.pos[1] > self.height :  # Adjust 50 based on the ball size
            self.ball.pos = (self.ball.pos[0], self.height )
            self.velocity_y = -self.velocity_y * self.damping  # Bounce with damping

        # Bounce off the left edge
        if self.ball.pos[0] < 0:
            self.ball.pos = (0, self.ball.pos[1])
            self.velocity_x = -self.velocity_x * self.damping  # Bounce with damping

        # Bounce off the right edge
        if self.ball.pos[0] > self.width - 50:  # Adjust 50 based on the ball size
            self.ball.pos = (self.width - 50, self.ball.pos[1])
            self.velocity_x = -self.velocity_x * self.damping  # Bounce with damping

    def on_touch_move(self, touch):
        # Adjust the horizontal velocity based on the touch movement
        self.velocity_x = touch.dx / 2.5  # You can adjust the division factor for sensitivity
        # Adjust the vertical velocity based on the mouse movement
        self.velocity_y = touch.dy / 2.5  # You can adjust the division factor for sensitivity

class BallApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')

        self.ball = Ball()
        self.label = Label(text='Move the mouse to throw the ball!\nBounce Count: 0', font_size='20sp')

        root.add_widget(self.label)
        root.add_widget(self.ball)

        # Schedule the update function to be called every 1/60 seconds (60 FPS)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

        return root

    def update(self, dt):
        # Update the ball's position
        self.ball.update(dt)

        # Update the label with the current bounce count
        self.label.text = f'Move the mouse to throw the ball!\nBounce Count: {self.ball.bounce_count}'

        # Change text color randomly if bounce count exceeds 200
        if self.ball.bounce_count > 200:
            random_color = [random.random() for _ in range(3)] + [1]
            self.label.color = random_color

if __name__ == '__main__':
    BallApp().run()
