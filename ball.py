from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.dropdown import DropDown
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

class BallSettings(SettingsWithSidebar):
    pass

class BallApp(App):
    def build(self):
        self.settings_cls = BallSettings
        self.use_kivy_settings = False  # Disable default settings panel

        root = Widget()

        # Add a background image to fill the entire screen
        self.background = Image(source='snowweather.jpg', allow_stretch=True, keep_ratio=False, size=(Window.width, Window.height))
        root.add_widget(self.background)

        self.ball = Ball()
        root.add_widget(self.ball)

        # Add theme selection button in the top-left corner
        background_button = Button(text='Background', size_hint=(None, None), pos=(10, Window.height - 50), size=(100, 50))
        background_button.bind(on_release=self.show_background_popup)
        root.add_widget(background_button)

        # Add skin selection button in the top-right corner
        skin_button = Button(text='Skin', size_hint=(None, None), pos=(Window.width - 110, Window.height - 50), size=(100, 50))
        skin_button.bind(on_release=self.show_skin_popup)
        root.add_widget(skin_button)

        # Schedule the update function to be called every 1/60 seconds (60 FPS)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

        return root

    def show_background_popup(self, instance):
        # Create a background selection popup
        content = BoxLayout(orientation='vertical')

        def set_background(instance, value):
            self.change_background(value)

        background_options = ['snow', 'forest']
        background_dropdown = DropDown()
        for background_option in background_options:
            btn = Button(text=background_option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: background_dropdown.select(btn.text))
            background_dropdown.add_widget(btn)

        background_button = Button(text='Select Background', size_hint=(None, None), height=44)
        background_button.bind(on_release=background_dropdown.open)
        background_dropdown.bind(on_select=lambda instance, x: set_background(instance, x))
        content.add_widget(background_button)

        popup = Popup(title='Background Selection', content=content, size_hint=(None, None), size=(300, 150))
        popup.open()

    def change_background(self, background_option):
        # Change background based on the selected option
        if background_option == 'snow':
            self.background.source = 'snowweather.jpg'
        elif background_option == 'forest':
            self.background.source = 'forest.jpg'

    def show_skin_popup(self, instance):
        # Create a skin selection popup
        content = BoxLayout(orientation='vertical')

        def set_skin(instance, value):
            self.change_skin(value)

        skin_options = ['red', 'green', 'blue']
        skin_dropdown = DropDown()
        for skin_option in skin_options:
            btn = Button(text=skin_option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: skin_dropdown.select(btn.text))
            skin_dropdown.add_widget(btn)

        skin_button = Button(text='Select Skin', size_hint=(None, None), height=44)
        skin_button.bind(on_release=skin_dropdown.open)
        skin_dropdown.bind(on_select=lambda instance, x: set_skin(instance, x))
        content.add_widget(skin_button)

        popup = Popup(title='Skin Selection', content=content, size_hint=(None, None), size=(300, 150))
        popup.open()

    def change_skin(self, skin_option):
        # Change ball color based on the selected option
        if skin_option == 'red':
            self.ball.ball_color.rgba = [1, 0, 0, 1]  # Red color
        elif skin_option == 'green':
            self.ball.ball_color.rgba = [0, 1, 0, 1]  # Green color
        elif skin_option == 'blue':
            self.ball.ball_color.rgba = [0, 0, 1, 1]  # Blue color

    def update(self, dt):
        # Update the ball's position
        self.ball.update(dt)

        # Change text color randomly if bounce count exceeds 200
        if self.ball.bounce_count > 200:
            random_color = [random.random() for _ in range(3)] + [1]
            self.label.color = random_color

if __name__ == '__main__':
    BallApp().run()
