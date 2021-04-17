#from kivy.uix.screenmanager import Screen

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

import guesser, plotter


#class AppBoxLayout(MDBoxLayout):
class AppBoxLayout(BoxLayout):
    stickguy = 'data/png/stick_4.png'
    numberline = 'data/last_numberline.png'

    img_stickguy = ObjectProperty(None)
    img_numberline = ObjectProperty(None)
    label_rem_guesses = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        # TODO: Get max_number from user input.
        self.max_number = 1000
        self.min_number = 1

        self.max_guesses = guesser.get_max_guesses(self.max_number)
        self.previous_guesses = []
        self.highest = self.max_number
        self.lowest = self.min_number
        self.num_guesses = 1
        self.num_remaining_guesses = -1
        self.current_limits = [self.lowest, self.highest]
        self.confidence = 50

    def handle_higher_clicked(self, button):
        if self.guesses_remaining():
            self.lowest = self.current_guess + 1
            self.current_limits = [self.lowest, self.highest]
            self.previous_guesses.append(self.current_guess)
            self.make_guess()
        else:
            # User wins.
            self.label_rem_guesses.text = f"Remaining guesses: 0"
            self.img_stickguy.source = 'data/png/stick_1.png'

    def handle_lower_clicked(self, button):
        if self.guesses_remaining():
            self.highest = self.current_guess - 1
            self.current_limits = [self.lowest, self.highest]
            self.previous_guesses.append(self.current_guess)
            self.make_guess()
        else:
            # User wins.
            self.label_rem_guesses.text = f"Remaining guesses: 0"
            self.img_stickguy.source = 'data/png/stick_1.png'

    def handle_check_clicked(self, button):
        # Stickguy wins.
        self.img_stickguy.source = 'data/png/stick_7.png'

    def make_guess(self):
        # Update Stickguy according to confidence level.
        num_rem_possibilities = self.highest + 1 - self.lowest
        self.num_remaining_guesses = self.max_guesses - self.num_guesses
        self.confidence = guesser.get_confidence(num_rem_possibilities, self.num_remaining_guesses)
        self.img_stickguy.source = self.get_stickguy()

        # Update number of remaining guesses.
        self.label_rem_guesses.text = f"Remaining guesses: {str(self.num_remaining_guesses)}"

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


#class StumpStickguyApp(MDApp):
class StumpStickguyApp(App):
    #max_dialog = None

    def build(self):
        # self.theme_cls.primary_palette = "LightBlue"
        # self.theme_cls.theme_style = "Dark"
        #screen = Screen()
        #return screen
        window = AppBoxLayout()
        window.make_guess()
        #return AppBoxLayout()
        return window

    """
    def show_max_dialog(self):
        if not self.max_dialog:
            self.max_dialog = MDDialog(
                text="Set maximum number:",
                buttons=[
                    MDFlatButton(text="CANCEL"),
                    MDFlatButton(text="SET"),
                ],
            )
        self.max_dialog.open()
    """

if __name__ == "__main__":
    StumpStickguyApp().run()
