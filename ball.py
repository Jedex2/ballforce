from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
from kivy.core.window import Window
import random

class Ball(Widget):
    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        with self.canvas:
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

        # Bounce off the left edge
        if self.ball.pos[0] < 0:
            self.ball.pos = (0, self.ball.pos[1])
            self.velocity_x = (-self.velocity_x * self.damping) / 2  # Apply damping
            self.on_side_bounce()

        # Bounce off the right edge
        if self.ball.pos[0] > Window.width - 50:  # Adjust 50 based on the ball size
            self.ball.pos = (Window.width - 50, self.ball.pos[1])
            self.velocity_x = (-self.velocity_x * self.damping) / 2  # Apply damping
            self.on_side_bounce()

        # Bounce when the ball hits the bottom of the screen
        if self.ball.pos[1] < 0:
            self.ball.pos = (self.ball.pos[0], 0)
            self.velocity_y = -self.velocity_y * self.damping  # Bounce with damping

    def on_side_bounce(self):
        self.bounce_count += 1
        if self.bounce_count % 10 == 0 or self.bounce_count >= 100:
            self.change_ball_color()

    def change_ball_color(self):
        # Change ball color to a random color
        random_color = [random.random() for _ in range(3)] + [1]
        self.ball_color.rgba = random_color

    def on_touch_move(self, touch):
        # Adjust the horizontal velocity based on the touch movement
        self.velocity_x = touch.dx / 2.5  # You can adjust the division factor for sensitivity
        # Adjust the vertical velocity based on the mouse movement
        self.velocity_y = touch.dy / 2.5  # You can adjust the division factor for sensitivity

class BallApp(App):
    def build(self):
        root = Widget()

        # Add a background image to fill the entire screen
        background = Image(source='snowweather.jpg', allow_stretch=True, keep_ratio=False, size=(Window.width, Window.height))
        root.add_widget(background)

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
