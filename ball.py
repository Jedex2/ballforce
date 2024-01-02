from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock

class Ball(Widget):
    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        with self.canvas:
            self.trail = []  # List to store trail ellipses
            Color(1, 0, 0, 1)  # Set color (red in RGBA) for the ball
            self.ball = Ellipse(pos=(self.center_x - 25, self.center_y - 25), size=(50, 50))

        self.velocity_x = 0  # Initial horizontal velocity
        self.velocity_y = 0  # Initial vertical velocity
        self.gravity = 1  # Gravity force

    def update(self, dt):
        # Apply gravity to the vertical velocity
        self.velocity_y -= self.gravity
        # Move the ball horizontally and vertically
        self.ball.pos = (self.ball.pos[0] + self.velocity_x, self.ball.pos[1] + self.velocity_y)

        # Bounce off the left edge
        if self.ball.pos[0] < 0:
            self.ball.pos = (0, self.ball.pos[1])
            self.velocity_x = -self.velocity_x

        # Bounce off the right edge
        if self.ball.pos[0] > self.width - 50:  # Adjust 50 based on the ball size
            self.ball.pos = (self.width - 50, self.ball.pos[1])
            self.velocity_x = -self.velocity_x

        # Bounce when the ball hits the bottom of the screen
        if self.ball.pos[1] < 0:
            self.ball.pos = (self.ball.pos[0], 0)
            self.velocity_y = -self.velocity_y * 0.5  # Bounce with some dampening

        # Update the trail
        self.update_trail()

    def update_trail(self):
        # Add a new ellipse with red color to the trail
        trail_size = 10
        with self.canvas:
            Color(1, 0, 0, 1)  # Set color (red in RGBA) for the trail
            new_ellipse = Ellipse(pos=self.ball.pos, size=(50, 50))

        self.trail.append(new_ellipse)

        # Limit the trail size
        if len(self.trail) > trail_size:
            old_ellipse = self.trail.pop(0)
            if old_ellipse in self.canvas.children:
                self.canvas.remove(old_ellipse)

    def on_touch_move(self, touch):
        # Adjust the horizontal velocity based on the touch movement
        self.velocity_x = touch.dx / 2  # You can adjust the division factor for sensitivity
        # Adjust the vertical velocity based on the mouse movement
        self.velocity_y = touch.dy / 2  # You can adjust the division factor for sensitivity

class BallApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')

        self.ball = Ball()
        self.label = Label(text='Move the mouse to throw the ball!', font_size='20sp')

        root.add_widget(self.label)
        root.add_widget(self.ball)

        # Schedule the update function to be called every 1/60 seconds (60 FPS)
        Clock.schedule_interval(self.update, 1.0 / 240.0)

        return root

    def update(self, dt):
        # Update the ball's position
        self.ball.update(dt)

if __name__ == '__main__':
    BallApp().run()
