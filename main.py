from button import InternalButton, ExternalButton
from elevator import Elevator

if __name__ == "__main__":
    e = Elevator()

    i_buttons = list(map(InternalButton, range(10)))
    e_buttons = list(map(ExternalButton, range(10)))

    for button in i_buttons + e_buttons:
        e.register(button)

    i_buttons[3].click()
    e.start()
    e_buttons[5].click()
    e_buttons[9].click()
    i_buttons[2].click()
    e.start()
