#from kivy.uix.screenmanager import Screen

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import guesser, plotter


class MaxPopup(Popup):
    user_input = ObjectProperty(None)

class AppBoxLayout(BoxLayout):
    stickguy = 'data/png/stick_4.png'
    numberline = ''

    img_stickguy = ObjectProperty(None)
    img_numberline = ObjectProperty(None)
    label_rem_guesses = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.min_number = 1
        self.previous_guesses = []
        self.lowest = self.min_number
        self.max_popup = MaxPopup()

    def handle_max_clicked(self, max_popup, user_max):
        self.max_number = self.verify_user_max(user_max)
        if not self.max_number:
            return
        self.set_initial_state(self.max_number)
        self.make_guess()
        self.max_popup = max_popup
        self.max_popup.dismiss()

    def handle_higher_clicked(self, button):
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
        # Stickguy wins.
        self.set_stickguy_wins()

    def handle_restart_clicked(self, button):
        # Remove the restart button.
        self.remove_widget(self.button_restart)
        # Restart the app.
        self.set_initial_state(self.max_number)
        self.make_guess()

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
        self.button_restart = Button()
        self.button_restart.text = "Play again?"
        self.button_restart.pos_hint = {'center_x': 0.5}
        self.button_restart.size_hint = 0.4, 0.08
        self.button_restart.bind(on_release=self.handle_restart_clicked)
        self.add_widget(self.button_restart, index=1)

    def update_label_remaining_guesses(self, rem_guesses):
        self.label_rem_guesses.text = f"Remaining guesses: {str(rem_guesses)}"

    def verify_user_max(self, user_max):
        try:
            max_num = int(''.join(filter(str.isdigit, user_max)))
        except ValueError:
            max_num = False
        return max_num


class StumpStickguyApp(App):

    def build(self):
        #screen = Screen()
        #return screen
        self.window = AppBoxLayout()
        return self.window

    def on_start(self):
        self.window.max_popup.open()


if __name__ == "__main__":
    StumpStickguyApp().run()
