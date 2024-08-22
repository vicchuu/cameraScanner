from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
#from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from plyer import camera
import traceback


class DebugApp(App):

    def build(self):
        try:
            self.screen_manager = ScreenManager()

            # Debug Screen
            debug_screen = Screen(name='debug')
            debug_layout = BoxLayout(orientation='vertical', padding=10)

            # Debug Label
            self.debug_label = TextInput(readonly=True, size_hint=(1, 0.9), background_color=(0, 0, 0, 1),
                                         foreground_color=(1, 1, 1, 1))
            debug_layout.add_widget(self.debug_label)

            # Button to proceed to main functionality
            btn_proceed = Button(text="Proceed to App", size_hint=(1, 0.1), background_color=(0.2, 0.6, 0.2, 1))
            btn_proceed.bind(on_press=self.go_to_home)
            debug_layout.add_widget(btn_proceed)

            debug_screen.add_widget(debug_layout)
            self.screen_manager.add_widget(debug_screen)

            # Home Screen
            self.create_home_screen()

            # Image Preview Screen
            preview_screen = Screen(name='preview')
            preview_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

            self.img = Image(size_hint=(1, 0.8))
            preview_layout.add_widget(self.img)

            btn_back = Button(text="Back to Home", size_hint=(1, 0.2), background_color=(0.8, 0.1, 0.1, 1))
            btn_back.bind(on_press=self.go_back_to_home)

            preview_layout.add_widget(btn_back)
            preview_screen.add_widget(preview_layout)

            self.screen_manager.add_widget(preview_screen)

            # Start with Debug Screen
            self.screen_manager.current = 'debug'

            return self.screen_manager

        except Exception as e:
            self.log_error("Application Build Error", e)
            return None

    def create_home_screen(self):
        try:
            home_screen = Screen(name='home')
            home_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

            btn_open_camera = Button(text="Take a Picture with Camera", size_hint=(1, 0.2),
                                     background_color=(0.1, 0.5, 0.8, 1))
            btn_open_camera.bind(on_press=self.open_camera)

            btn_upload_image = Button(text="Upload an Image from Device", size_hint=(1, 0.2),
                                      background_color=(0.1, 0.5, 0.1, 1))
            btn_upload_image.bind(on_press=self.open_file_chooser)

            home_layout.add_widget(btn_open_camera)
            home_layout.add_widget(btn_upload_image)
            home_screen.add_widget(home_layout)

            self.screen_manager.add_widget(home_screen)
        except Exception as e:
            self.log_error("Home Screen Initialization Error", e)
            self.screen_manager.current = 'debug'

    def go_to_home(self, instance):
        try:
            self.screen_manager.current = 'home'
        except Exception as e:
            self.log_error("Transition to Home Screen Error", e)
            self.screen_manager.current = 'debug'

    def open_camera(self, instance):
        try:
            camera.take_picture(filename='captured_image.png', on_complete=self.display_image)
        except Exception as e:
            self.log_error("Camera Error", e)
            self.screen_manager.current = 'debug'

    def display_image(self, filepath):
        try:
            if filepath:
                self.img.source = filepath
                self.img.reload()
                self.screen_manager.current = 'preview'
        except Exception as e:
            self.log_error("Image Display Error", e)
            self.screen_manager.current = 'debug'

    def open_file_chooser(self, instance):
        try:
            filechooser_popup = Popup(title='Choose an Image',
                                      content=self.create_file_chooser(),
                                      size_hint=(0.9, 0.9))
            filechooser_popup.open()
        except Exception as e:
            self.log_error("File Chooser Error", e)
            self.screen_manager.current = 'debug'

    def create_file_chooser(self):
        try:
            filechooser_layout = BoxLayout(orientation='vertical')
            file_chooser = FileChooserIconView(filters=["*.png", "*.jpg", "*.jpeg"])
            file_chooser.bind(on_selection=self.on_file_selected)

            filechooser_layout.add_widget(file_chooser)
            return filechooser_layout
        except Exception as e:
            self.log_error("File Chooser Creation Error", e)
            self.screen_manager.current = 'debug'
            return BoxLayout()  # Return an empty layout as fallback

    def on_file_selected(self, filechooser, selection):
        try:
            if selection:
                self.display_image(selection[0])
        except Exception as e:
            self.log_error("File Selection Error", e)
            self.screen_manager.current = 'debug'

    def go_back_to_home(self, instance):
        try:
            self.screen_manager.current = 'home'
        except Exception as e:
            self.log_error("Navigation Error", e)
            self.screen_manager.current = 'debug'

    def log_error(self, context, exception):
        try:
            error_message = f"Error in {context}:\n{traceback.format_exc()}\n"
            self.debug_label.text += error_message
            print(error_message)  # For console logging during debugging
        except Exception as e:
            print(f"Logging Error: {traceback.format_exc()}")  # Ensure logging itself does not fail

if __name__ == '__main__':
    try:
        DebugApp().run()
    except Exception as e:
        print(f"Fatal Application Error: {traceback.format_exc()}")
