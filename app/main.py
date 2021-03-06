#from kivy.uix.screenmanager import Screen

import time

from kivy.app import App
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import guesser, plotter
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')

class MaxPopup(Popup):
    user_input = ObjectProperty(None)

class IntroPopup(Popup):
    pass

class AppBoxLayout(BoxLayout):
    stickguy = 'data/png/stick_4.png'
    numberline = ''

    img_stickguy = ObjectProperty(None)
    img_numberline = ObjectProperty(None)
    label_rem_guesses = ObjectProperty(None)
    label_hint = ObjectProperty(None)
    btn_icon_ch = ObjectProperty(None)
    btn_icon_up = ObjectProperty(None)
    btn_icon_dn = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.min_number = 1
        self.previous_guesses = []
        self.lowest = self.min_number
        self.max_popup = MaxPopup()
        self.intro_popup = IntroPopup()

    def handle_max_release(self, max_popup, button, user_max):
        button.background_color = [0, 0, 0, 1]
        self.max_number, text = self.verify_user_max(user_max)
        self.max_popup = max_popup
        if not self.max_number:
            self.max_popup.user_input.hint_text = text
            self.max_popup.user_input.text = ''
            return
        self.max_popup.dismiss(animation=False)
        self.intro_popup.open()

    def handle_intro_dismiss(self):
        self.set_initial_state(self.max_number)
        self.make_guess()

    def handle_higher_clicked(self, button):
        if self.label_hint:
            self.remove_widget(self.label_hint)
        if self.current_guess == self.highest:
            # User made a mistake (or is being cheeky?).
            self.set_stickguy_wins()
        elif self.guesses_remaining():
            self.lowest = self.current_guess + 1
            self.current_limits = [self.lowest, self.highest]
            self.previous_guesses.append(self.current_guess)
            self.make_guess()
        else:
            # User wins.
            self.set_user_wins()

    def handle_lower_clicked(self, button):
        if self.label_hint:
            self.remove_widget(self.label_hint)
        if self.current_guess == self.lowest:
            # User made a mistake (or is being cheeky?).
            self.set_stickguy_wins()
        elif self.guesses_remaining():
            self.highest = self.current_guess - 1
            self.current_limits = [self.lowest, self.highest]
            self.previous_guesses.append(self.current_guess)
            self.make_guess()
        else:
            # User wins.
            self.set_user_wins()

    def handle_check_clicked(self, button):
        if self.label_hint:
            self.remove_widget(self.label_hint)
        # Stickguy wins.
        self.set_stickguy_wins()

    def handle_restart_clicked(self, button):
        # Remove the restart button.
        self.remove_widget(self.button_restart)
        # Start a new round.
        self.img_numberline.source = ''
        self.img_numberline.reload()
        self.intro_popup = IntroPopup()
        self.max_popup = MaxPopup()
        self.max_popup.open()

    def make_guess(self):
        # Update Stickguy according to confidence level.
        num_rem_possibilities = self.highest + 1 - self.lowest
        self.num_remaining_guesses = self.get_num_remaining_guesses()
        self.confidence = guesser.get_confidence(num_rem_possibilities, self.num_remaining_guesses)
        self.img_stickguy.source = self.get_stickguy()

        # Update number of remaining guesses.
        self.update_label_remaining_guesses(str(self.num_remaining_guesses))

        # Update the numberline.
        guess_min, guess_max = guesser.set_guess_range(self.lowest, self.highest)
        self.current_guess = guesser.get_guess(guess_min, guess_max)
        plotter.draw_numberline(
            self.min_number,
            self.max_number,
            self.previous_guesses,
            self.current_limits,
            self.current_guess,
        )
        self.img_numberline.reload()
        self.num_guesses += 1

    def guesses_remaining(self):
        return not self.num_guesses >= self.max_guesses

    def get_num_remaining_guesses(self):
        num_remaining_guesses = self.max_guesses - self.num_guesses
        return num_remaining_guesses

    def get_stickguy(self):
        if self.confidence > 65:
            stickguy = 'data/png/stick_6.png'
        elif self.confidence > 55:
            stickguy = 'data/png/stick_5.png'
        elif self.confidence > 45:
            stickguy = 'data/png/stick_4.png'
        elif self.confidence > 35:
            stickguy = 'data/png/stick_3.png'
        else:
            stickguy = 'data/png/stick_2.png'
        return stickguy

    def set_initial_state(self, user_max):
        self.btn_icon_ch.disabled = False
        self.btn_icon_up.disabled = False
        self.btn_icon_dn.disabled = False
        self.lowest = self.min_number
        self.previous_guesses = []

        self.numberline = 'data/last_numberline.png'
        self.img_numberline.source = self.numberline

        self.max_guesses = guesser.get_max_guesses(self.max_number)
        self.num_remaining_guesses = self.max_guesses

        self.highest = self.max_number
        self.current_limits = [self.lowest, self.highest]

        self.num_guesses = 1

    def set_stickguy_wins(self):
        self.img_stickguy.source = 'data/png/stick_7.png'
        self.show_button_restart()

    def set_user_wins(self):
        self.label_rem_guesses.text = f"Remaining guesses: 0"
        self.img_stickguy.source = 'data/png/stick_1.png'
        self.show_button_restart()

    def show_button_restart(self):
        self.btn_icon_ch.disabled = True
        self.btn_icon_up.disabled = True
        self.btn_icon_dn.disabled = True
        self.button_restart = Button()
        self.button_restart.text = "Play again?"
        self.button_restart.pos_hint = {'center_x': 0.5}
        self.button_restart.size_hint = 0.4, 0.08
        self.button_restart.bind(on_release=self.handle_restart_clicked)
        self.add_widget(self.button_restart, index=1)

    def update_label_remaining_guesses(self, rem_guesses):
        self.label_rem_guesses.text = f"Remaining guesses: {str(rem_guesses)}"

    def verify_user_max(self, user_max):
        text = "any whole number > 2"
        if len(user_max) > 19:
            # Too many characters for numpy.
            text = 'fewer than 19 characters, please'
            max_num = False
        else:
            try:
                max_num = int(''.join(filter(str.isdigit, user_max)))
                if max_num < 3:
                    max_num = False
            except ValueError:
                max_num = False
        return max_num, text


class StumpStickguyApp(App):

    def build(self):
        self.window = AppBoxLayout()
        return self.window

    def on_start(self):
        self.window.max_popup.open()


if __name__ == "__main__":
    StumpStickguyApp().run()
