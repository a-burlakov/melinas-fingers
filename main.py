"""
Entrypoint to application.
"""

from pynput import keyboard

from services.ui import start_application, pynput_on_press, pynput_on_release


def pynput_listener_start() -> None:

    # Starting 'pynput' listener to read player's keypresses.
    listener = keyboard.Listener(on_press=pynput_on_press, on_release=pynput_on_release)
    listener.start()


if __name__ == '__main__':

    pynput_listener_start()

    start_application()
