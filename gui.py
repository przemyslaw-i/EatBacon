#!/usr/bin/env python

"""
GUI for Eat Bacon.
"""

__author__ = "Przemyslaw I."
__copyright__ = "Copyright 2022, Przemyslaw I."
__license__ = "MIT"
__version__ = "0.1.0"

from threading import Timer
from eat_bacon import EatBacon
from gui_helpers import label, button, entry, window, question_box

class Gui:
    """
    Provides GUI window.
    """

    DESIRED_STATUSES = [1,3,7] # Statuses, that are considered "running"

    def __init__(self):
        """
        Initializes Tk and Prepares variables.
        """
        # Window
        self._eb_win, self._frm = window()
        # Variables
        self._widgets = {}
        self._timer = None
        self._last_status = 7
        self._eb = None

    def init_widgets(self):
        """
        Creates all Window components.
        """
        # URL
        self._widgets["url_lbl"] = label(self._frm, (0, 0), "Beacon URL:")
        self._widgets["url_entry"] = entry(self._frm, (1, 0), 25, 12, '')

        # Sleep
        self._widgets["sleep_lbl"] = label(self._frm, (0, 1), "Sleep time:")
        self._widgets["sleep_entry"] = entry(self._frm, (1, 1), 25, 12, '2')

        # Buttons
        self._widgets["control_btn"] = button(
            self._frm, (0, 2), "Start", self.start_stop_click
        )
        self._widgets["quit_btn"] = button(
            self._frm, (1, 2), "Quit", self.quit_click
        )

        # Application status
        self._widgets["app_stat"] = label(
            self._frm, (0, 3), "Eat Bacon is disabled..."
        )
        self._widgets["app_stat"].grid(columnspan=2, pady=(0, 20))
        self._widgets["app_stat"].configure(fg='red')

        # Stats labels
        lbl_data = [
            ("Status:", "Unknown", "status"),
            ("Distance:", "0.00m", "dist"),
            ("Moving time:", "0s", "moving"),
            ("Elapsed time:", "0s", "elapsed"),
            ("Battery:", "0%", "batt")
        ]
        count = 0
        for lbl in lbl_data:
            # Create name label
            self._widgets[f"{lbl[2]}_lbl"] = label(
                self._frm, (0, count+4), lbl[0], ("", 12, "bold")
            )
            # Create value label
            self._widgets[f"{lbl[2]}_val_lbl"] = label(
                self._frm, (1, count+4), lbl[1]
            )
            count += 1

    def execute_timer(self):
        """
        Executes Beacon datapoint gathering and parsing.
        """
        # Get & parse datapoint
        dtp = self._eb.get_datapoint()
        bacon = EatBacon.parse_datapoint(dtp)
        # Set status
        self._last_status = bacon[0]
        # Update GUI if not cancelled
        if self._timer:
            self._widgets["status_val_lbl"].configure(
                text=self._eb.get_status(bacon[0])
            )
            self._widgets["dist_val_lbl"].configure(text=f"{bacon[1]:.2f}m")
            self._widgets["moving_val_lbl"].configure(text=f"{bacon[4]}s")
            self._widgets["elapsed_val_lbl"].configure(text=f"{bacon[5]}s")
            self._widgets["batt_val_lbl"].configure(text=f"{bacon[6]}%")
        # Make output
        self._eb.make_output(bacon)
        # Set next timer
        self.start_timer()

    def run(self):
        """
        Executes main Window event loop.
        """
        # Main loop
        self._eb_win.mainloop()

    def start_timer(self):
        """
        Creates EatBacon object, starts Timer executions loop and
        disabled controls.
        """
        # New object if not existing
        if not self._eb:
            # Create object
            self._eb = EatBacon(self._widgets['url_entry'].get())
            # If not initialized
            if not self._eb.get_init_call():
                # Abort start
                self._eb = None
                return
        # Only, when last status show valid state
        if self._last_status in Gui.DESIRED_STATUSES:
            # Create and start timer
            self._timer = Timer(
                int(self._widgets['sleep_entry'].get()), self.execute_timer
            )
            self._timer.start()
            # Change text of button and label
            self._widgets['control_btn'].configure(text='Stop')
            self._widgets["app_stat"].configure(
                text = "Eat Bacon is enabled...",
                fg = 'green'
            )
            # Disable inputs
            self._widgets["sleep_entry"].configure(state='disabled')
            self._widgets["url_entry"].configure(state='disabled')
        # If status not valid
        else:
            # Stop the timer
            self.stop_timer()

    def stop_timer(self):
        """
        Stops timer, restores controls and variables.
        """
        # Only, when timer is created
        if self._timer:
            # Stop timer
            self._timer.cancel()
            self._timer = None
        # Change text of button and label
        self._widgets['control_btn'].configure(text='Start')
        self._widgets["app_stat"].configure(
            text = "Eat Bacon is disabled...",
            fg = 'red'
        )
        # Enable inputs
        self._widgets["sleep_entry"].configure(state='normal')
        self._widgets["url_entry"].configure(state='normal')
        # Set previous state
        self._eb = None
        self._last_status = 7

    def quit(self):
        """
        Gracefuly exits application
        """
        if self._timer:
            self.start_stop_click()
        self._eb_win.destroy()

    def quit_click(self):
        """
        Implements Quit button click action.
        """
        # If Timer is working
        if self._timer:
            # Ask question
            question_box(
                'Exit Application',
                'Beacon is running. Are you sure, you want to close?',
                self.quit
            )
        else:
            self.quit()

    def start_stop_click(self):
        """
        Implements Start/Stop button click action.
        """
        if self._timer:
            self.stop_timer()
        else:
            self.start_timer()

if __name__ == '__main__':
    # Execute GUI
    gui = Gui()
    gui.init_widgets()
    gui.run()
