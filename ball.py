from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.dropdown import DropDown
from kivy.core.audio import SoundLoader
from kivy.uix.image import AsyncImage  # Import AsyncImage
import random

class Ball(Widget):
    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.bounce_sound = None  # Initialize bounce sound to None
        self.bounce_count = 0  # Initialize bounce count
        self.velocity_x = 0  # Initial horizontal velocity
        self.velocity_y = 0  # Initial vertical velocity
        self.gravity = 1  # Gravity force
        self.damping = 0.9  # Damping factor for reducing velocity on each bounce

        # Load the initial bounce sound (icebounce.mp3)
        self.load_bounce_sound('icebounce.mp3')

        with self.canvas:
            self.ball_color = Color(0, 1, 1, 1)  # Set color (cyan in RGBA) for the ice ball
            self.ball = Ellipse(pos=(self.center_x - 25, self.center_y - 25), size=(50, 50))
            self.canvas.add(self.ball_color)

    def load_bounce_sound(self, sound_file):
        # Load the bounce sound effect
        self.bounce_sound = SoundLoader.load(sound_file) if sound_file else None

    def play_bounce_sound(self):
        if self.bounce_sound:
            self.bounce_sound.volume = 1.0  # Adjust the volume (0.0 to 1.0)
            self.bounce_sound.play()

    def on_side_bounce(self, skin_color):
        self.bounce_count += 1
        self.change_ball_color(skin_color)
        self.play_bounce_sound()

    def change_ball_color(self, skin_color):
        # Change ball color to the selected skin color
        self.ball_color.rgba = skin_color

    def update(self, dt):
        # Apply gravity to the vertical velocity
        self.velocity_y -= self.gravity

        # Move the ball horizontally and vertically
        self.ball.pos = (self.ball.pos[0] + self.velocity_x, self.ball.pos[1] + self.velocity_y)

        # Bounce off the left edge
        if self.ball.pos[0] < 0:
            self.ball.pos = (0, self.ball.pos[1])
            self.velocity_x = (-self.velocity_x * self.damping) / 2  # Apply damping
            self.on_side_bounce(self.ball_color.rgba)

        # Bounce off the right edge
        if self.ball.pos[0] > Window.width - 50:  # Adjust 50 based on the ball size
            self.ball.pos = (Window.width - 50, self.ball.pos[1])
            self.velocity_x = (-self.velocity_x * self.damping) / 2  # Apply damping
            self.on_side_bounce(self.ball_color.rgba)

        # Bounce when the ball hits the bottom of the screen
        if self.ball.pos[1] < 0:
            self.ball.pos = (self.ball.pos[0], 0)
            self.velocity_y = -self.velocity_y * self.damping  # Bounce with damping

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

        # Load background music
        self.background_music = None
        self.load_game_sounds()

        return root

    def load_game_sounds(self):
        # Load additional game sounds
        self.bounce_sound_3 = SoundLoader.load('autumnsound.mp3')
        self.bounce_sound_2 = SoundLoader.load('cold.mp3')

    def show_skin_popup(self, instance):
        # Create a skin selection popup
        content = BoxLayout(orientation='vertical')

        def set_skin(instance, value):
            self.change_skin(value)

        skin_options = ['Ice Ball', 'forest Ball', 'Lava ball']
        skin_images = ['Ice ball.jpg', 'forest ball.png', 'lava ball.png']

        skin_dropdown = DropDown()

        for skin_option, skin_image in zip(skin_options, skin_images):
            btn = Button(text=skin_option, size_hint_y=None, height=44)
            img = AsyncImage(source=skin_image, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, img=img: skin_dropdown.select(img.source))
            skin_dropdown.add_widget(btn)

        skin_button = Button(text='Select Skin', size_hint=(None, None), height=44)
        skin_button.bind(on_release=skin_dropdown.open)
        skin_dropdown.bind(on_select=lambda instance, x: set_skin(instance, x))
        content.add_widget(skin_button)

        popup = Popup(title='Skin Selection', content=content, size_hint=(None, None), size=(300, 200))
        popup.open()

    def change_skin(self, skin_option):
        # Change ball appearance based on the selected option
        skin_images = {
            'Ice ball.png': [0, 1, 1, 1],
            'forest ball.png': [0, 1, 0, 1],
            'lava ball.png': [0, 0, 1, 1]
        }

        skin_color = skin_images.get(skin_option, [0, 1, 1, 1])

        self.ball.load_bounce_sound(f'{skin_option}_bounce.mp3')  # Adjust sound file names accordingly
        self.ball.change_ball_color(skin_color)  # Update ball color
        self.ball.on_side_bounce(skin_color)  # Trigger bounce with updated color

    def update(self, dt):
        # Update the ball's position
        self.ball.update(dt)

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
            self.load_game_sounds_for_background('snow')
            self.play_background_music('cold.mp3')
        elif background_option == 'forest':
            self.background.source = 'forest.jpg'
            self.load_game_sounds_for_background('forest')
            self.play_background_music('autumnsound.mp3')

    def load_game_sounds_for_background(self, background):
        # Load game sounds based on the selected background
        if background == 'snow':
            self.bounce_sound_2 = SoundLoader.load('cold.mp3')
            self.bounce_sound_3 = SoundLoader.load('cold.mp3')
        elif background == 'forest':
            self.bounce_sound_2 = SoundLoader.load('autumnsound.mp3')
            self.bounce_sound_3 = SoundLoader.load('autumnsound.mp3')

    def play_background_music(self, music_file):
        # Stop the current background music if playing
        if self.background_music:
            self.background_music.stop()

        # Load and play the new background music
        self.background_music = SoundLoader.load(music_file)
        if self.background_music:
            self.background_music.loop = True
            self.background_music.play()

if __name__ == '__main__':
    BallApp().run()
